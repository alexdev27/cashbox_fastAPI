from base_cashbox_config import save_to_json, base_cashbox_config_dict


def make_pirit2f_config():
    config = base_cashbox_config_dict(device_name='pirit2f')
    config['comport'] = str(input('\t' + 'Введите ком-порт к которому подключен пирит (COM5 например): ')).strip()
    config['comportSpeed'] = int(str(input('\t' + 'Введите скорость обмена данными (узнать в настройках пирита): ')).strip())
    save_to_json(config)


make_pirit2f_config()


