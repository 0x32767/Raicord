from __future__ import annotations

from typing import TYPE_CHECKING, Callable
import dearpygui.dearpygui as dpg

if TYPE_CHECKING:
    from wrapers import DiscordAccount, Guild, Channel, Message

from wrapers import create_message_profile, create_embed_profile
from webbrowser import open_new_tab
from json import dumps


class GUI:
    def __init__(self) -> None:
        self.get_messages: Callable[[int], dict] = None
        self.send_message: Callable[[int]] = None
        self.open_channels: list[str] = []

    def update_user(self, ud: DiscordAccount) -> None:
        with dpg.window(label="User info", no_close=True):
            dpg.add_text(f"Username: {ud.username!r} -> {ud.global_name}")
            dpg.add_text(f"Id: {ud.id}")
            dpg.add_text(ud.bio)

    def update_guilds(self, gd: list[Guild]):
        with dpg.window(label="Guilds", no_close=True):
            for guild in gd:
                dpg.add_button(
                    label=guild.name,
                    callback=self.show_guild,
                    tag=f"show_{guild.id}",
                )

                if guild.description is not None:
                    dpg.add_text(f"{guild.description!r}")

                if guild.join_data is not None:
                    dpg.add_text(f"Joined on: {guild.join_data}")

                dpg.add_text(f"Members: {guild.member_count}")
                dpg.add_text(f"Owner: {guild.owner}")
                dpg.add_text()

                self.render_guild(guild)

    def show_guild(self, caller: str | int, app_data, _):
        dpg.show_item(caller.removeprefix("show_"))

    def on_close_channel(self, caller, app_data, data: str):
        self.open_channels.remove(data)

    def view_channel(self, caller: str, app_data, data: tuple[Channel, Guild]):
        self.open_channels.append(data[0].id)

        with dpg.window(
            label=f"Channel {data[0].name}",
            tag=f"channel_{data[0].id}",
            on_close=self.on_close_channel,
            user_data=data[0].id,
        ):
            for msg in reversed(self.get_messages(data[0].id)):
                self.render_message(msg)

            dpg.add_input_text(
                on_enter=True,
                callback=self.send_msg_callback,
                user_data=data[0].id,
                tag=f"send_message_inp_{data[0].id}",
            )

    def add_channel_message(self, msg: dict):
        self.render_message(msg, before=f"send_message_inp_{msg['channel_id']}")

    def send_msg_callback(self, caller: str, app_data, user_data: str):
        self.send_message(user_data, app_data)
        dpg.set_value(f"send_message_inp_{user_data}", "")

    def render_guild(self, guild: Guild):
        with dpg.window(label=f"{guild.name!r}", show=False, tag=guild.id):
            # metta data
            # with dpg.child_window(label="Extra Info"):
            #     dpg.add_text(f"")

            # channels
            with dpg.child_window(label="Channels"):
                for channel in guild.channels:
                    if channel.type != 0:
                        continue

                    dpg.add_button(
                        label=(channel.name + " | " + channel.id),
                        callback=self.view_channel,
                        user_data=(channel, guild),
                    )

                    if channel.topic:
                        dpg.add_text(channel.topic)

                    else:
                        dpg.add_text("no description")

                    dpg.add_text()

    def view_json(self, caller, app_data, user_data):
        with dpg.window(label="JSON of message"):
            dpg.add_text(user_data)

    def view_attachment(self, caller, app_data, attachment_data):
        def open_attachment(caller_, app_data_, url):
            open_new_tab(url)

        with dpg.window(label="View attachment"):
            dpg.add_text(f"Type: {attachment_data['content_type']}")
            dpg.add_text(f"File: {attachment_data['filename']}")
            dpg.add_text(f"Link: {attachment_data['url']}")
            dpg.add_button(
                label="View",
                callback=open_attachment,
                user_data=attachment_data["url"],
            )

    def render_message(self, data, before=0):
        msg = create_message_profile(data)

        with dpg.group(before=before):
            dpg.add_text(msg.author["username"])

            # if the content is blank then we end up adding a blank line
            if msg.content:
                dpg.add_text(msg.content)

            for attachment in msg.attachments:
                dpg.add_button(
                    label="View attachment",
                    callback=self.view_attachment,
                    user_data=attachment,
                )

            for embed in data["embeds"]:
                with dpg.child_window(height=100):
                    em = create_embed_profile(embed)

                    dpg.add_text(f"{em.title}")
                    dpg.add_text(f"Type: {em.type}")
                    dpg.add_text(f"{em.description}")
                    dpg.add_text(f"{em.url!r}")

            dpg.add_button(
                label="See JSON",
                callback=self.view_json,
                user_data=dumps(data, indent=2),
            )

            dpg.add_text()

    def run(self):
        dpg.create_context()

        dpg.create_viewport(title="XCord", width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

        dpg.destroy_context()


if __name__ == "__main__":
    GUI().run()
