# quotexapi_patch.py
import requests
import websocket
import json
import threading
import time

class Quotex:
    def __init__(self, laravel_session=None):
        self.websocket = None
        self.ssid = None
        self.laravel_session = laravel_session
        self.profile_data = None
        self.connected = False

    def connect(self):
        if not self.laravel_session:
            raise Exception("Missing laravel_session")

        headers = {
            "Cookie": f"laravel_session={self.laravel_session}"
        }
        response = requests.get("https://qxbroker.com/en/demo-trade", headers=headers)
        if response.status_code != 200:
            raise Exception("Login failed or invalid laravel_session cookie.")

        self.websocket = websocket.WebSocketApp(
            "wss://ws.qxbroker.com/socket.io/?EIO=3&transport=websocket",
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
        )
        self.ws_thread = threading.Thread(target=self.websocket.run_forever)
        self.ws_thread.start()
        time.sleep(3)
        self.connected = True

    def _on_open(self, ws):
        print("[WebSocket Opened]")

    def _on_error(self, ws, error):
        print("[WebSocket Error]", error)

    def _on_message(self, ws, message):
        if "42[\"profile" in message:
            try:
                payload = json.loads(message[2:])[1]
                self.profile_data = payload
            except Exception as e:
                print("Error parsing profile data:", e)

    def get_profile(self):
        if not self.connected:
            raise Exception("WebSocket not connected")
        self.websocket.send('42["get-profile",{}]')
        time.sleep(2)
        return self.profile_data or {}

    def buy(self, amount, asset, direction="call", duration=60):
        if not self.connected:
            raise Exception("WebSocket not connected")
        trade_payload = {
            "amount": amount,
            "asset": asset,
            "direction": direction,
            "duration": duration,
            "type": "demo"
        }
        self.websocket.send(f'42["buy",{json.dumps(trade_payload)}]')
        return {"status": "sent", "trade": trade_payload}
