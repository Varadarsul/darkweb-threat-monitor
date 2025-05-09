import requests
from stem import Signal
from stem.control import Controller
import time
import logging

class TorSession:
    def __init__(self, tor_password=None):
        self.session = requests.session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.tor_password = tor_password
        self.last_identity_change = time.time()
        
    def get(self, url, **kwargs):
        """Make a GET request through Tor"""
        try:
            return self.session.get(url, **kwargs)
        except Exception as e:
            logging.error(f"Error making request to {url}: {str(e)}")
            return None
            
    def get_new_identity(self):
        """Change Tor identity"""
        if time.time() - self.last_identity_change < 10:
            return False
            
        try:
            with Controller.from_port(port=9051) as controller:
                if self.tor_password:
                    controller.authenticate(password=self.tor_password)
                else:
                    controller.authenticate()
                controller.signal(Signal.NEWNYM)
                self.last_identity_change = time.time()
                return True
        except Exception as e:
            logging.error(f"Error changing Tor identity: {str(e)}")
            return False
            
    def post(self, url, **kwargs):
        """Make a POST request through Tor"""
        try:
            response = self.session.post(url, **kwargs)
            return response
        except Exception as e:
            logging.error(f"Failed to make POST request to {url}: {str(e)}")
            return None 