from pyrogram.types import InlineKeyboardMarkup
from appeals.core.common import (
    Buttons,
    Common,
    safe_call
)

async def start_command(message):
    user = message.from_user
    if Common.waiting_for_input.get(user.id):
        return
    buttons = []
    buttons.append([Buttons.create_conversion, Buttons.conversions_list])
    if getattr(message, 'data', None) is not None:
        await safe_call(
            message.message.edit_text,
            text="Здравствуйте! Выберите действие:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await safe_call(
            message.reply_text,
            text="Здравствуйте! Выберите действие:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def start_msg(_, message):
    await start_command(message)


async def start_cb(_, callback_query):
    user = callback_query.from_user
    state = Common.waiting_for_input.get(user.id)
    if state:
        Common.waiting_for_input.pop(user.id, None)
    await start_command(callback_query)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
