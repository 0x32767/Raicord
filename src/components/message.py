from .base_component import BaseComponent
import dearpygui.dearpygui as dpg


class Message(BaseComponent):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, str | int]) -> None:
        self._data = data

    def render(self):
        with dpg.group():
            dpg.add_button(label=f"{self._data['author']['username']}")
            dpg.add_text(self._data["content"])

    def send(self, data: dict[str, str | int]):
        ...
