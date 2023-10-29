from wrapers import create_account_profile, create_guild_profile
from listener import DiscordListener
from gui import GUI
import threading


class MyDiscordClient(DiscordListener):
    def __init__(self, token: str, gui: GUI):
        super().__init__(token)
        self.ui: GUI = gui
        self.user_data = None

        self.ui.get_user_prof = self.get_user_data
        self.ui.get_messages = self.get_messages
        self.ui.send_message = self.send

    def on_READY(self, e):
        self.user_data = create_account_profile(e["user"])
        self.ui.update_user(self.user_data)

        self.guilds = [create_guild_profile(g) for g in e["guilds"]]
        self.ui.update_guilds(self.guilds)

    def on_MESSAGE_CREATE(self, e):
        # The user has a channel open and a message is sent in it
        if str(e["channel_id"]) in self.ui.open_channels:
            self.ui.add_channel_message(e)

    def get_user_data(self, user_id: str):
        res = self.client.get(
            f"https://discord.com/api/v9/users/{user_id}",
            headers={
                "authorization": self.token,
                "Content-Type": "application/json",
            },
        )
        return res.json()

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
