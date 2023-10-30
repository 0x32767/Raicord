from __future__ import annotations

from .base_component import BaseComponent
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING
from .channel import Channel


if TYPE_CHECKING:
    from gui import GUI


class ChannelList(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, str | int]) -> None:
        self._data = data

    def render(self, ui: GUI):
        for channel in self._data:
            ui.register_component(Channel(channel)).render(ui)
            dpg.add_spacer(height=10)
