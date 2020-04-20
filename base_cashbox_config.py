import json


def base_cashbox_config_dict(device_name='Default'):
    config = {}
    print(f'\n\tСоздание конфига для: {device_name}')
    print('\t' + '-'*20)
    config['deviceName'] = device_name
    config['timezone'] = str(input('\t' + 'Введите часовой пояс: ')).strip()
    config['cashName'] = str(input('\t' + 'Введите название кассы: ')).strip()
    config['shopNumber'] = int(str(input('\t' + 'Введите номер магазина: ')).strip())
    config['department'] = int(str(input('\t' + 'Введите департамент: ')).strip())
    config['paygateAddress'] = str(input('\t' + 'Введите адрес плятежного шлюза (ip:port или доменное имя): ')).strip()
    return config


def save_to_json(config_dict):
    print('\t' + 'Сохранение...')
    with open('cash-conf.json', 'w') as file:
        json.dump(config_dict, file)
    print('\t' + 'Сохранено в cash-conf.json')
