from mongoengine.errors import DoesNotExist, ValidationError

from app.exceptions import CashboxException


def get_model_by_id_or_raise(model, model_id, include_nested=False, nested_deep=1):
    try:
        if include_nested:
            return model.objects.get(id=model_id).select_related(max_depth=nested_deep)
        else:
            return model.objects.no_dereference().get(id=model_id)
    except (DoesNotExist, ValidationError):
        msg = f'No such element with id of ({model_id})'
        raise CashboxException(data=msg, to_logging=msg)
