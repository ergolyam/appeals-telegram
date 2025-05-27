import httpx
from pyrogram.types import InlineKeyboardButton


class Common():
    http = httpx.AsyncClient(timeout=30)
    waiting_for_input = {}


class Buttons():
    create_conversion = InlineKeyboardButton(
        text="📄 Написать обращение 📄",
        callback_data="create_conversion"
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
