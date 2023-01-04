import configparser
import app.cisco as cisco
import app.palo as palo


# Function to compile instances of Palo class objects from config file
def palo_compile():
    try:
        devices = []
        config = configparser.ConfigParser()
        config.read('config/paloalto.ini')
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")
    
    try:
        for section in config.sections():
            devices.append(palo.Palo(
                config[section]['name'],
                config[section]['api'],
                config[section]['ip']
                ))
    except Exception as e:
        raise RuntimeError(f"Error creating devices: {e}")
    
    return devices

# Function to compile Cisco class objects from config file
def cisco_compile():
    try:
        devices = []
        config = configparser.ConfigParser()
        config.read('config/cisco.ini')
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")
    
    try:
        for section in config.sections():
            devices.append(cisco.Cisco(
                config[section]['name'],
                config[section]['ip'],
                config[section]['user'],
                config[section]['key'],
                config[section]['prompt']
                ))
    except Exception as e:
        raise RuntimeError(f"Error creating devices: {e}")
        
    return devices