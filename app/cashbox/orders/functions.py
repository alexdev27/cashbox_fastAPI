from copy import deepcopy
from app.kkt_device.decorators import validate_kkt_state, kkt_comport_activation, \
    check_for_opened_shift_in_fiscal
from app import KKTDevice
from app.cashbox.main_cashbox.models import Cashbox
from app.exceptions import CashboxException
from app.enums import DocumentTypes, PaymentChoices, PaygateURLs, \
    get_cashbox_tax_from_fiscal_tax, get_fiscal_tax_from_cashbox_tax
from app.helpers import generate_internal_order_id, get_cheque_number, \
    round_half_down, round_half_up, get_WIN_UUID
from .schemas import PaygateOrderSchema, ConvertToResponseCreateOrder, OrderSchema
from .models import Order
from config import CASH_SETTINGS as CS
from app.logging import logging_decorator
from pprint import pprint as pp


@logging_decorator('order_logs.log', 'order_logger')
@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def create_order(*args, **kwargs):
    cashbox = Cashbox.box()
    # raise CashboxException(data='Holy Shield')
    if not cashbox.cash_character:
        msg = 'Символ кассы отсутствует. Зарегистрируйте'
        raise CashboxException(data=msg)

    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']
    cashier_name = req_data['cashier_name']
    cashier_id = req_data['cashier_id']
    payment_type = req_data['payment_type']
    document_type = DocumentTypes.PAYMENT.value
    amount_entered = req_data['amount_entered']
    wares = req_data['wares']
    character = cashbox.cash_character
    real_money = False
    order_prefix = f'{character}-'

    if req_data['payment_type'] == PaymentChoices.CASH:
        wares = find_and_modify_one_ware_with_discount(wares)
        real_money = True

    wares = _build_wares(wares)

    kkt_kwargs = {
        'cashier_name': cashier_name,
        'payment_type': payment_type,
        'document_type': document_type,
        'order_prefix': order_prefix,
        'amount_entered': amount_entered,
        'wares': wares
    }

    created_order = KKTDevice.handle_order(**kkt_kwargs)

    data_to_db = {
        'cashier_name': cashier_name,
        'cashier_id': cashier_id,
        'clientOrderID': generate_internal_order_id(),
        'amount': created_order['total_without_discount'],
        'amount_with_discount': created_order['transaction_sum'],
        'creation_date': created_order['datetime'],
        'cashID': cashbox.cash_id,
        'checkNumber': get_cheque_number(created_order['check_number']),
        'doc_number': created_order['doc_number'],
        'cardHolder': created_order.get('cardholder_name', ''),
        'pan': created_order.get('pan_card', ''),
        'payLink': created_order.get('rrn', ''),
        'payType': payment_type,
        'paid': 1,
    }

    if real_money:
        cashbox.update_shift_money_counter(DocumentTypes.PAYMENT, created_order['transaction_sum'])

    # data_to_db.update({'wares': _build_wares(wares)})
    order, errs = OrderSchema().load({**kkt_kwargs, **data_to_db})

    to_paygate, _errs = PaygateOrderSchema().dump(order)
    to_paygate.update({'proj': cashbox.project_number})
    to_paygate.update({'url': PaygateURLs.new_order})
    cashbox.add_order(order)
    cashbox.save_paygate_data_for_send(to_paygate)

    to_response, errs = ConvertToResponseCreateOrder().load(
        {'device_id': get_WIN_UUID(), **kkt_kwargs, **data_to_db}
    )
    return to_response


@logging_decorator('order_logs.log', 'order_logger')
@kkt_comport_activation()
@validate_kkt_state()
@check_for_opened_shift_in_fiscal()
async def return_order(*args, **kwargs):
    req_data, kkt_info = kwargs['valid_schema_data'], kwargs['opened_port_info']

    cashier_name = req_data['cashier_name']
    cashier_id = req_data['cashier_id']
    order_uuid = req_data['internal_order_uuid']
    doc_type = DocumentTypes.RETURN.value
    cashbox = Cashbox.box()
    order = Order.objects(clientOrderID=order_uuid).first()

    if not order:
        msg = 'Нет такого заказа'
        raise CashboxException(data=msg)
    print('flag  ', order.returned)
    if order.returned:
        msg = 'Этот заказ уже был возвращен'
        raise CashboxException(data=msg)

    order_dict = OrderSchema().dump(order).data
    kkt_kwargs = {
        'cashier_name': cashier_name,
        'document_type': doc_type,
        'payment_type': order_dict['payType'],
        'wares': order_dict['wares'],
        'amount_entered': order_dict['amount_with_discount'],
        'pay_link': order_dict['payLink'],
        'order_prefix': order_dict['order_prefix']
    }

    canceled_order = KKTDevice.handle_order(**kkt_kwargs)

    cashbox.update_shift_money_counter(DocumentTypes.RETURN, order_dict['amount_with_discount'])

    order.returned = True
    order.return_cashier_name = cashier_name
    order.return_cashier_id = cashier_id
    order.return_date = canceled_order['datetime']
    order.save().reload()

    to_paygate = PaygateOrderSchema(only=[
        'clientOrderID', 'cashID', 'checkNumber'
    ]).dump(order).data
    to_paygate.update({'proj': cashbox.project_number})
    to_paygate.update({'url': PaygateURLs.cancel_order})
    cashbox.save_paygate_data_for_send(to_paygate)
    return {}


@logging_decorator('order_logs.log', 'order_logger')
async def round_price(*args, **kwargs):
    req_data = kwargs['valid_schema_data']
    data = find_and_modify_one_ware_with_discount(req_data, True)
    return data


def find_and_modify_one_ware_with_discount(wares, get_only_one_discounted_product=False):

    _wares = deepcopy(wares)
    total_sum = 0
    for w in _wares:
        total_sum = round_half_down(w['price'] * w['quantity'] + total_sum, 2)

    num_dec = round_half_down(float(str(total_sum-int(total_sum))[1:]), 2)

    item = max(_wares, key=lambda x: x['price'])

    if not num_dec:
        if get_only_one_discounted_product:
            return {'discountedPrice': 0, 'barcode': item['barcode'],
                    'discountedSum': 0, 'orderSum': total_sum,
                    'discountedOrderSum': total_sum}
        else:
            return wares

    disc_price = round_half_down(item['price'] - num_dec, 2)
    total_sum_with_discount = round_half_down(total_sum - num_dec, 2)

    if item['quantity'] == 1:
        item.update({'discountedPrice': disc_price})
        item.update({'discount': num_dec})
    if item['quantity'] > 1:
        new_ware = deepcopy(item)
        item.update({'quantity': item['quantity'] - 1})
        item.update({'discountedPrice': 0})
        new_ware.update({'discountedPrice': disc_price})
        new_ware.update({'discount': num_dec})
        new_ware.update({'quantity': 1})
        _wares.append(new_ware)

    if get_only_one_discounted_product:
        _item = max(_wares, key=lambda x: x.get('discountedPrice', 0))
        return {'barcode': _item['barcode'],
                'discountedPrice': _item['discountedPrice'],
                'discountedSum': num_dec,
                'orderSum': total_sum,
                'discountedOrderSum': total_sum_with_discount}

    return _wares


def _build_wares(wares):
    _wares = []
    copied_wares = deepcopy(wares)
    for ware in copied_wares:
        # tax_rate = get_cashbox_tax_from_fiscal_tax(int(ware['tax_number']))
        tax_rate = int(ware['tax_rate'])
        divi = float(f'{1}.{tax_rate // 10}')
        multi = tax_rate / 100
        price_for_all = round_half_down(ware.get('discountedPrice') or ware['price'] * ware['quantity'], 2)
        tax_sum = round_half_up(price_for_all / divi * multi, 2)

        ware.update({'priceDiscount': ware.get('discountedPrice') or ware['price']})
        ware.update({'taxRate': tax_rate})
        ware.update({'taxSum': tax_sum})
        ware.update({'tax_number': get_fiscal_tax_from_cashbox_tax(tax_rate)})
        ware.update({'amount': price_for_all})
        ware.update({'department': CS['department']})
        _wares.append(ware)

    return _wares
