import websocket
import threading
import pprint
import httpx
import time
import json


class DiscordListener:
    def __init__(self, token: str):
        self.pp = pprint.PrettyPrinter()
        self.client = httpx.Client()
        self.token = token

    def send_json_request(self, ws, request):
        ws.send(json.dumps(request))

    def recieve_json_response(self, ws):
        response = ws.recv()

        if response:
            return json.loads(response)

        return None

    def heartbeat(self, interval, ws):
        print("Heartbeat start")
        while True:
            time.sleep(interval)
            heartbeatJSON = {"op": 1, "d": "null"}

            self.send_json_request(ws, heartbeatJSON)
            print("heartbeat sent")

    def send(self, chid: int, msg: str):
        self.client.post(
            f"https://discord.com/api/v9/channels/{chid}/messages",
            data=json.dumps({"content": msg}),
            headers={
                "authorization": self.token,
                "Content-Type": "application/json",
            },
        ).text

    def start(self):
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=6&encording=json")

        event = self.recieve_json_response(ws)

        heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
        threading._start_new_thread(self.heartbeat, (heartbeat_interval, ws))

        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {"$os": "arch", "$browser": "fire fox", "$device": "pc"},
            },
        }

        self.send_json_request(ws, payload)

        while True:
            event = self.recieve_json_response(ws)

            if event["t"] is None:
                continue

            try:
                getattr(self, "on_" + event["t"])(event["d"])

            except AttributeError:
                print(event["t"], "not accounted for")


if __name__ == "__main__":
    listener = DiscordListener()
    listener.start()
