from __future__ import annotations

from .base_component import BaseComponent
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING
from .guild import Guild

if TYPE_CHECKING:
    from gui import GUI


class GuildList(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: list[dict[str, str | int]]) -> None:
        self._data = data

    def render(self, ui: GUI):
        with dpg.window(label="Server List", no_close=True):
            for guild in self._data:
                ui.register_component(Guild.from_json(guild)).render(ui)
                dpg.add_text()
