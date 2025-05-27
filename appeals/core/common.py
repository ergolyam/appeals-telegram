import httpx, asyncio
from enum import Enum
from typing import cast
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors import FloodWait


class Common():
    http = httpx.AsyncClient(timeout=30)
    waiting_for_input = {}


class Buttons():
    create_conversion = InlineKeyboardButton(
        text="📄 Написать обращение 📄",
        callback_data="create_conversion"
    )
    conversions_list = InlineKeyboardButton(
        text="🔍 Текущие обращения 🔎",
        callback_data="conversions_list"
    )
    back_to_menu = InlineKeyboardButton(
        text="⬅️ На главную",
        callback_data="back_to_menu"
    )


class ConversionStatus(Enum):
    unviewed = ("unviewed", "🆕")
    accepted = ("accepted", "✅")
    progress = ("progress",  "🔄")
    executed = ("executed",  "🏁")
    closed = ("closed",    "🔒")

    def __init__(self, code: str, emoji: str) -> None:
        self.code  = code
        self.emoji = emoji

    def __str__(self) -> str:
        return self.code



async def safe_call(func, *args, **kwargs):
    for _ in range(5):
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            wait_sec: int = cast(int, e.value)
            await asyncio.sleep(wait_sec + 1)
    raise


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
