import httpx, asyncio
from enum import Enum
from typing import cast
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors import FloodWait


class Common():
    http = httpx.AsyncClient(timeout=30)
    waiting_for_input = {}
    file_input = {}


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
    skip_files = InlineKeyboardButton(
        text="🚫 Пропустить 🚫",
        callback_data="skip_files"
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


class DummyCallbackQuery:
    def __init__(self, *, msg, data):
        self.id = "local-test"
        self.from_user = msg.from_user
        self.chat_instance = "dummy"
        self.message = msg
        self.data = data

    async def answer(self, *args, **kwargs):
        return True

def get_callback_data(
        message,
        target_text: str
):
    kb = getattr(
        message.reply_markup,
        "inline_keyboard",
        None
    )
    if kb is None:
        return None

    for row in kb:
        for button in row:
            if button.text == target_text:
                return button.callback_data

    return None


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
