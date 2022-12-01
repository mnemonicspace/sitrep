# Base class
class Device:
    def __init__(self, ip, platform, user, key):

        # Run setters to initialize values
        self.ip = ip
        self.platform = platform
        self.user = user
        self.key = key

        # IP of device
        @property
        def ip(self):
            return self._ip

        @ip.setter
        def ip(self, ip):
            if not ip:
                raise ValueError("No IP Provided")

            self._ip = ip

        # Maunufacturer Platform
        @property
        def platform(self):
            return self._platform

        @platform.setter
        def platform(self, platform):
            if not platform:
                raise ValueError("No Platform Provided")

            self._platform = platform

        # SSH Keyfile location
        @property
        def key(self):
            return self._key

        @key.setter
        def key(self, key):
            if not key:
                raise ValueError("Invalid Key File")

            self._key = key

        # User account to use for device connections
        @property
        def user(self):
            return self._user

        @user.setter
        def user(self, user):
            if not user:
                raise ValueError("No User Provided")

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


# Function to initialize new Device objects
def create(ip, platform, user, key="~./ssh/test"):
    return Device(ip, platform, key, user)
