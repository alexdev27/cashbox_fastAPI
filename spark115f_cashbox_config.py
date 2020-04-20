from base_cashbox_config import save_to_json, base_cashbox_config_dict


def make_spark115f_config():
    config = base_cashbox_config_dict(device_name='spark115f')
    save_to_json(config)


make_spark115f_config()
