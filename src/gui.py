from __future__ import annotations

from typing import TYPE_CHECKING
import dearpygui.dearpygui as dpg
from components import *


class GUI:
    def __init__(self, token: str) -> None:
        self.token = token
        self.components = []

    def update_user(self, ud: dict[str, str | int]) -> None:
        ud_component = UserDataComponent(ud)
        ud_component.render(self)
        self.components.append(ud_component)

    def update_guilds(self, gd: list[dict[str, str | int]]):
        gd_component = GuildList(gd)
        gd_component.render(self)
        self.components.append(gd_component)

    def register_component(self, component):
        self.components.append(component)
        return component

    def run(self):
        dpg.create_context()

        dpg.create_viewport(title="XCord", width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

        dpg.destroy_context()


if __name__ == "__main__":
    GUI().run()
