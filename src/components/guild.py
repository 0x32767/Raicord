from __future__ import annotations

from .base_component import BaseComponent
from .channel_list import ChannelList
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gui import GUI


class Guild(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, str | int]) -> None:
        self._data = data

    def show_hide_metta_data(self, sender, app_data, user_data):
        if app_data:
            dpg.show_item(f"metta_data_{self._data['id']}")

        else:
            dpg.hide_item(f"metta_data_{self._data['id']}")

    def show_guild(self, sender, app_data, user_data: GUI):
        with dpg.window(label=self._data["name"]):
            dpg.add_checkbox(
                label="Show metta data",
                callback=self.show_hide_metta_data,
            )

            with dpg.child_window(tag=f"metta_data_{self._data['id']}", show=False):
                for k, v in self._data.items():
                    if isinstance(v, (str, int)):
                        dpg.add_text(f"{k!r} : {v!r}")

            with dpg.child_window():
                user_data.register_component(
                    ChannelList(self._data["channels"])
                ).render(user_data)

    def show_admin(self, sender, app_data, user_data: GUI):
        ...

    def render(self, ui: GUI):
        dpg.add_button(
            label=self._data["name"],
            callback=self.show_guild,
            user_data=ui,
        )

        if self._data["description"] is not None:
            dpg.add_text(self._data["description"])

        if self._data["joined_at"] is not None:
            dpg.add_text(f'Joined on: {self._data["joined_at"]!r}')

        dpg.add_text(
            f"Member count: {self._data['member_count']}",
        )
        dpg.add_button(
            label=f"Owner: {self._data['owner_id']}",
            callback=self.show_admin,
            user_data=ui,
        )
