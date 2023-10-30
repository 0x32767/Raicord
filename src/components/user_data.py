from __future__ import annotations

from .base_component import BaseComponent
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gui import GUI


class UserDataComponent(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, str | int]) -> None:
        self._data = data

    def render(self, ui: GUI):
        with dpg.window(label="User info", no_close=True):
            dpg.add_text(f"Global name: {self._data['global_name']!r}")
            dpg.add_text(f"Username: {self._data['username']!r}")
            dpg.add_text(f"Id: {self._data['id']}")
            dpg.add_text(self._data["bio"])
