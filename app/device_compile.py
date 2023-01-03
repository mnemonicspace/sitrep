import configparser
import app.nhcisco as nhcisco
import app.nhpalo as nhpalo


def palo_compile():
    devices = []
    config = configparser.ConfigParser()
    config.read('config/paloalto.ini')
    
    for section in config.sections():
        devices.append(nhpalo.Palo(
            config[section]['name'],
            config[section]['api'],
            config[section]['ip']
            ))
    return devices

def cisco_compile():
    devices = []
    config = configparser.ConfigParser()
    config.read('config/cisco.ini')
    
    for section in config.sections():
        devices.append(nhcisco.Cisco(
            config[section]['name'],
            config[section]['ip'],
            config[section]['user'],
            config[section]['key'],
            config[section]['prompt']
            ))
    return devices