import configparser
import app.cisco as cisco
import app.palo as palo
import pathlib


# Function to compile instances of Palo class objects from config file
def palo_compile():
    try:
        path = pathlib.Path(__file__).parent.resolve()
        devices = []
        config = configparser.ConfigParser()
        config.read(f"{path}/../config/paloalto.ini")
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
        path = pathlib.Path(__file__).parent.resolve()
        devices = []
        config = configparser.ConfigParser()
        config.read(f"{path}/../config/cisco.ini")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")
    
    try:
        for section in config.sections():
            try:
                enable_prompt = config[section]['enable_prompt']
                enable_pass = config[section]['enable_pass']
                enable_level = config[section]['enable_level']
            except KeyError:
                enable_prompt = ''
                enable_pass = ''
                enable_level = '15'
            devices.append(cisco.Cisco(
                config[section]['name'],
                config[section]['ip'],
                config[section]['user'],
                config[section]['key'],
                config[section]['prompt'],
                enable_prompt,
                enable_pass,
                enable_level
                ))
    except Exception as e:
        raise RuntimeError(f"Error creating devices: {e}")
        
    return devices