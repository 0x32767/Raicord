from discord_api.listener import DiscordListener
from gui import GUI
import threading


class MyDiscordClient(DiscordListener):
    def __init__(self, token: str, gui: GUI):
        super().__init__(token)
        self.ui: GUI = gui

    def on_READY(self, e):
        self.ui.update_user(e["user"])
        self.ui.update_guilds(e["guilds"])

    def on_MESSAGE_CREATE(self, e):
        # The user has a channel open and a message is sent in it
        if str(e["channel_id"]) in self.ui.open_channels:
            self.ui.add_channel_message(e)


with open("token.txt", "r") as f:
    token = f.read()

ui = GUI(token)
listener = MyDiscordClient(token, ui)

threading._start_new_thread(listener.ui.run, ())
listener.start()
