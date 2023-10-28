from dataclasses import dataclass
from pprint import pprint


@dataclass
class DiscordAccount:
    username: str
    id: str
    global_name: str
    email: str
    discriminator: str
    bio: str


def create_account_profile(data):
    return DiscordAccount(
        data["username"],
        data["id"],
        data["global_name"],
        data["email"],
        data["discriminator"],
        data["bio"],
    )


@dataclass
class Channel:
    topic: str
    name: str
    id: str
    type: int


def create_channel_profile(data: dict):
    return Channel(
        data.get("topic", "no-topic"),
        data["name"],
        data["id"],
        data["type"],
    )


@dataclass
class Guild:
    name: str
    description: str
    member_count: str
    owner: str
    join_data: str
    id: str
    channels: list[Channel]


def create_guild_profile(data):
    return Guild(
        data["name"],
        data["description"],
        data["member_count"],
        data["owner_id"],
        data["joined_at"],
        data["id"],
        [create_channel_profile(d) for d in data["channels"]],
    )


@dataclass
class Embed:
    title: str
    type: str
    description: str
    url: str | None


def create_embed_profile(data: dict):
    return Embed(
        data.get("title", "..."),
        data.get("type", "..."),
        data.get("description", "..."),
        data.get("url", "..."),
    )


@dataclass
class Message:
    author: str
    id: str
    content: str
    attachments: list[dict]


def create_message_profile(data):
    return Message(
        data["author"],
        data["id"],
        data["content"],
        data["attachments"],
    )
