from pexpect import pxssh
import re
from os.path import exists

# class for cisco objects
class Cisco:
    def __init__(self, name: str, ip: str, user: str, key: str, prompt: str, enable_prompt: str = '', enable_pass: str = '', enable_level: str = '15'):

        # Run setters to initialize values
        self.name = name
        self.ip = ip
        self.user = user
        self.key = key
        self.prompt = prompt
        self.enable_prompt = enable_prompt
        self.enable_pass = enable_pass
        self.enable_level = enable_level

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

        # user regex to check for valid IP
        valid = re.findall(
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

        if len(valid) != 1:
            raise ValueError("Invalid IP Provided")
        else:
            self._ip = ip

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

    # cli prompt of device's non config mode
    @prompt.setter
    def prompt(self, prompt):
        if not prompt:
            raise ValueError("Invalid Prompt Provided")

        self._prompt = prompt
    
    @property
    def enable_prompt(self):
        return self._enable_prompt

    # cli prompt of device's config mode
    @enable_prompt.setter
    def enable_prompt(self, enable_prompt):
        self._enable_prompt = enable_prompt
    
    @property
    def enable_pass(self):
        return self._enable_pass

    # cli prompt of device's config mode
    @enable_pass.setter
    def enable_pass(self, enable_pass):
        self._enable_pass = enable_pass
        
    @property
    def enable_level(self):
        return self._enable_level

    # cli prompt of device's config mode
    @enable_level.setter
    def enable_level(self, enable_level):
        self._enable_level = enable_level
        
    # Function to send command to device
    def send_cmd(self, cmd):
        try:
            ssh_options = {'IdentityFile': f"{self.key}"}
            connection = pxssh.pxssh(options=ssh_options)
            connection.login(self.ip, self.user,
                            original_prompt=self.prompt, auto_prompt_reset=False)
            
            # if enable credentials provided, try to enable, otherwise expect config mode
            if self.enable_prompt and self.enable_pass:
                connection.sendline(f"enable {self.enable_level}")
                connection.expect_exact('Password:')
                connection.sendline(self.enable_pass)
                connection.expect_exact(self.enable_prompt)
                prompt = self.enable_prompt
            else:
                connection.prompt()
                prompt = self.prompt
            
            connection.sendline(cmd)
            connection.expect_exact(prompt)
            response = connection.before.decode()
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")
