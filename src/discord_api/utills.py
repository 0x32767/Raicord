from httpx import Client


def get_user_data(client: Client, user_id: str, token: str):
    res = client.get(
        f"https://discord.com/api/v9/users/{user_id}",
        headers={
            "authorization": token,
            "Content-Type": "application/json",
        },
    )
    return res.json()


def get_messages(client: Client, channel_id: int, token: str):
    res = client.get(
        f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50",
        headers={
            "authorization": token,
            "Content-Type": "application/json",
        },
    )
    return res.json()
