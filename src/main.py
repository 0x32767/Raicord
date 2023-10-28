from wrapers import create_account_profile, create_guild_profile
from listener import DiscordListener
from gui import GUI
import threading


class MyDiscordClient(DiscordListener):
    def __init__(self, token: str, gui: GUI):
        super().__init__(token)
        self.ui: GUI = gui
        self.user_data = None

        self.ui.get_messages = self.get_messages
        self.ui.send_message = self.send

    def on_READY(self, e):
        self.user_data = create_account_profile(e["user"])
        self.ui.update_user(self.user_data)

        self.guilds = [create_guild_profile(g) for g in e["guilds"]]
        self.ui.update_guilds(self.guilds)

    def get_messages(self, channel_id: int):
        res = self.client.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50",
            headers={
                "authorization": self.token,
                "Content-Type": "application/json",
            },
        )
        return res.json()

    @property
    def gui(self):
        return self.ui


with open("token.txt", "r") as f:
    token = f.read()

listener = MyDiscordClient(token, GUI())

threading._start_new_thread(listener.gui.run, ())
listener.start()
