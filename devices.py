#import netmiko
import re
from os.path import exists

# Base class


class Device:
    def __init__(self, name, ip, platform, user, key):

        # Run setters to initialize values
        self.name = name
        self.ip = ip
        self.platform = platform
        self.user = user
        self.key = key


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Invalid Name Provided")

        self._name = name

    # IP of device
    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        if not isinstance(ip, str):
            raise ValueError("Invalid IP Provided")

        valid = re.findall(
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)
        if len(valid) != 1:
            raise ValueError("Invalid IP Provided")
        else:
            self._ip = ip

    # Maunufacturer Platform
    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, platform):
       
        platforms = ["paloalto_panos", "cisco_ios"]
       
        if platform not in platforms or not isinstance(platform, str):
            raise ValueError("Invalid Platform Provided")

        self._platform = platform

    # SSH Keyfile location
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if not key or not isinstance(key, str) or not exists(key):
            raise ValueError("Invalid Key File")

        self._key = key

    # User account to use for device connections
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if not user or not isinstance(user, str):
            raise ValueError("Invalid User Provided")

        self._user = user

    # Method to build netmiko compatible device object
    def build(self):
        return {
            "device_type": self.platform,
            "host": self.ip,
            "username": self.user,
            "use_keys": True,
            "key_file": self.key,
        }

    # Function to send command to device

#    def send_cmd(self, cmd):
#
#        # Netmiko run command
#        with netmiko.ConnectHandler(**self.build()) as net_connect:
#            return net_connect.send_command(cmd)


# Function to initialize new Device objects
def create(name, ip, platform, user, key="/Users/msexton/.ssh/ansible"):
    return Device(name, ip, platform, user, key)
