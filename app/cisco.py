from pexpect import pxssh
import re
from os.path import exists

# Base class
class Cisco:
    def __init__(self, name: str, ip: str, user: str, key: str, prompt: str):

        # Run setters to initialize values
        self.name = name
        self.ip = ip
        self.user = user
        self.key = key
        self.prompt = prompt

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("No name provided")
        self._name = name

    # IP of device
    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        if not ip:
            raise ValueError("No IP Provided")

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

        platforms = ["paloalto_panos", "cisco_ios", "linux"]

        if platform not in platforms:
            raise ValueError("Invalid Platform Provided")

        self._platform = platform

    # SSH Keyfile location
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if not exists(key):
            raise ValueError("Invalid Key File")

        self._key = key

    # User account to use for device connections
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if not user:
            raise ValueError("Invalid User Provided")

        self._user = user

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, prompt):
        if not prompt:
            raise ValueError("Invalid Prompt Provided")

        self._prompt = prompt

    # Function to send command to device
    def send_cmd(self, cmd):
        try:
            ssh_options = {'IdentityFile': f"{self.key}"}
            connection = pxssh.pxssh(options=ssh_options)
            connection.login(self.ip, self.user,
                            original_prompt=self.prompt, auto_prompt_reset=False)
            connection.sendline(cmd)
            connection.expect('#')
            response = connection.before.decode()
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")
