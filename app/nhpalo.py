import re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Palo:
    def __init__(self, name: str, api: str, ip: str):
        self.name = name
        self.api = api
        self.ip = ip
        self.url = f"https://{self.ip}/api/"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("No name provided")
        self._name = name
        
    @property
    def api(self):
        return self._api
    
    @api.setter
    def api(self, api):
        if not api:
            raise ValueError("No name provided")
        self._api = api
        
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
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url
                
    def send_xpath(self, path):
        try:
            uri = f"?type=op&cmd={path}&key={self.api}"
            request = f"{self.url}{uri}"
            response = requests.get(request, verify=False)
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")
