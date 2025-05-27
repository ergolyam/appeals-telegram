from pyrogram.types import InlineKeyboardMarkup
from appeals.core.common import Buttons, Common


async def start_command(_, message):
    user = message.from_user
    if Common.waiting_for_input.get(user.id):
        return
    buttons = []
    buttons.append([Buttons.create_conversion])
    await message.reply_text(
        text="Здравствуйте! Выберите действие:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )



if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
