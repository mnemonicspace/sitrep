import re
import requests
import urllib3

# disable warnings for self signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# class for palo alto objects
class Palo:
    def __init__(self, name: str, api: str, ip: str):
        # run setters to initiate values
        self.name = name
        self.api = api
        self.ip = ip
        self.url = f"https://{self.ip}/api/"
    
    # name of device
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("No name provided")
        self._name = name

    # api key    
    @property
    def api(self):
        return self._api
    
    @api.setter
    def api(self, api):
        if not api:
            raise ValueError("No name provided")
        self._api = api

    # ip address    
    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        if not ip:
            raise ValueError("No IP Provided")

        # use regex to check for valid IP
        valid = re.findall(
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

        if len(valid) != 1:
            raise ValueError("Invalid IP Provided")
        else:
            self._ip = ip
    
    # url for api endpoint
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url

    # class method to send XML api xpaths            
    def send_xpath(self, path):
        try:
            uri = f"?type=op&cmd={path}&key={self.api}"
            request = f"{self.url}{uri}"
            response = requests.get(request, verify=False)
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")
