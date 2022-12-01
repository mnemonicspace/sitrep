class Device:
    def __init__(self, ip, platform, user, key):

        self.ip = ip
        self.platform = platform
        self.user = user
        self.key = key

        @property
        def ip(self):
            return self._ip

        @ip.setter
        def ip(self, ip):
            if not ip:
                raise ValueError("No IP Provided")

            self._ip = ip

        @property
        def platform(self):
            return self._platform

        @platform.setter
        def platform(self, platform):
            if not platform:
                raise ValueError("No Platform Provided")

            self._platform = platform

        @property
        def key(self):
            return self._key

        @key.setter
        def key(self, key):
            if not key:
                raise ValueError("Invalid Key File")

            self._key = key

        @property
        def user(self):
            return self._user

        @user.setter
        def user(self, user):
            if not user:
                raise ValueError("No User Provided")

            self._user = user

    def build(self):
        return {
            "device_type": self.platform,
            "host": self.ip,
            "username": self.user,
            "use_keys": True,
            "key_file": self.key,
        }


def create(ip, platform, user, key="~./ssh/test"):
    return Device(ip, platform, key, user)
