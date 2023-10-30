from __future__ import annotations

from discord_api.utills import get_messages
from .base_component import BaseComponent
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING
from .message import Message
from httpx import Client

if TYPE_CHECKING:
    from gui import GUI


class Channel(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, str | int]) -> None:
        self._data: dict[str, str | int] = data

    def open_channel(self, sender, app_data, user_data: tuple[str, GUI]):
        with Client() as cl:
            msgs = get_messages(cl, self._data["id"], user_data[0])

        with dpg.window(label=f"Channel {self._data['name']}"):
            for msg in msgs:
                user_data[1].register_component(Message(msg)).render()
                dpg.add_spacer(height=10)

    def view_channel_data(self, sender, app_data, user_data):
        with dpg.window(label=f"Channel metta data"):
            for k, v in self._data.items():
                dpg.add_text(f"{k} : {v}")

    def render(self, ui: GUI):
        dpg.add_button(
            label=self._data["name"],
            callback=self.open_channel,
            user_data=(ui.token, ui),
        )
        dpg.add_text(self._data.get("topic", "no-topic"))
        dpg.add_text(
            {
                0: "GUILD_TEXT",
                1: "DM",
                2: "GUILD_VOICE",
                3: "GROUP_DM",
                4: "GUILD_CATEGORY",
                5: "GUILD_ANNOUNCEMENT",
                10: "ANNOUNCEMENT_THREAD",
                11: "PUBLIC_THREAD",
                12: "PRIVATE_THREAD",
                13: "GUILD_STAGE_VOICE",
                14: "GUILD_DIRECTORY",
                15: "GUILD_FORUM",
                16: "GUILD_MEDIA",
            }[self._data["type"]]
        )
