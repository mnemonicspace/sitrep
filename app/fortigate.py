import re
import requests
import urllib3

# disable warnings for self signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# class for palo alto objects
class Fortigate:
    def __init__(self, name: str, api: str, ip: str, primary:str, secondary:str):
        # run setters to initiate values
        self.name = name
        self.api = api
        self.ip = ip
        self.primary = primary
        self.secondary = secondary
        self.url = f"https://{self.ip}/api/v2/"
    
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
        
    # name of pair devices
    @property
    def primary(self):
        return self._primary
    
    @primary.setter
    def name(self, primary):
        if not primary:
            raise ValueError("No primary name provided")
        self._primary = primary
        
    @property
    def secondary(self):
        return self._secondary
    
    @name.setter
    def secondary(self, secondary):
        if not secondary:
            raise ValueError("No secondary name provided")
        self._secondary = secondary
        

    # class method to get the active hostname           
    def get_hostname(self):
        try:
            uri = f"monitor/system/status/?access_token={self.api}"
            request = f"{self.url}{uri}"
            response = requests.get(request, verify=False)
            return re.findall(r'hostname":"(.*?)",', str(response.text))[0]
            
        except Exception as e:
            raise RuntimeError(f"{e}")