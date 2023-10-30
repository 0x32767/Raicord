from abc import ABC, abstractmethod


class BaseComponent(ABC):
    @abstractmethod
    def __init__(self, data: dict[str, str | int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError

    def send(self, data: dict[str, str | int]):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data):
        return cls(data)
