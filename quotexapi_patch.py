
from quotexapi.stable_api import Quotex as OriginalQuotex
import requests

class Quotex(OriginalQuotex):
    def __init__(self, laravel_session: str):
        super().__init__(ssid=None)
        self.laravel_session = laravel_session
        self.session = requests.Session()
        self.session.cookies.set('laravel_session', laravel_session)
    
    def connect(self):
        self.websocket_client.headers['Cookie'] = f"laravel_session={self.laravel_session}"
        return super().connect()
