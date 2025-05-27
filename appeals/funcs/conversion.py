from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from appeals.core.common import (
    Common,
    Buttons,
    ConversionStatus,
    safe_call
)
from appeals.api.conversion import (
    post_conversion,
    get_conversions,
    get_conversion
)
from appeals.config import logging_config
logging = logging_config.setup_logging(__name__)


async def create_conversion(_, callback_query):
    user = callback_query.from_user
    buttons = []
    buttons.append([Buttons.back_to_menu])
    Common.waiting_for_input[user.id] = {"step": "head"}
    await safe_call(
        callback_query.message.reply,
        text="Введите <b>заголовок</b> (до 32 символов):",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


async def create_conversion_text(_, message):
    user = message.from_user
    state = Common.waiting_for_input.get(user.id)

    if not state:
        await safe_call(
            message.reply,
            text="Введите /start, чтобы начать."
        )
        return

    if state["step"] == "head":
        head = message.text.strip()
        buttons = []
        buttons.append([Buttons.back_to_menu])

        if len(head) > 32:
            await safe_call(
                message.reply,
                text="❗️ Заголовок слишком длинный (максимум 32 символа). Попробуйте ещё раз."
            )
            return

        state.update({"step": "text", "head": head})
        await safe_call(
            message.reply,
            text="Теперь введите <b>основное сообщение</b>:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    if state["step"] == "text":
        head = state["head"]
        text = message.text

        r = await post_conversion(
            user_id=user.id,
            head=head,
            text=text
        )
        logging.debug(f"{user.id} - response: {r}")

        await safe_call(
            message.reply,
            text="✅ Сообщение обработано!"
        )
        Common.waiting_for_input.pop(user.id, None)
        return


async def conversions_list(_, callback_query):
    user = callback_query.from_user
    r = await get_conversions(user.id)

    buttons = []
    for item in r:
        status = ConversionStatus[item["status"]]
        text = f"{status.emoji} {item['head']}"
        buttons.append(
            [InlineKeyboardButton(
                text=text,
                callback_data=f"conv:{item['id']}"
            )]
        )
    buttons.append([Buttons.back_to_menu])
    
    await safe_call(
        callback_query.message.edit_text,
        text="Ваши обращения:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


async def conversions_view(_, callback_query):
    user = callback_query.from_user
    conv_id = int(callback_query.data.split(":")[1])
    buttons = []
    buttons.append([Buttons.back_to_menu])
    r = await get_conversion(
        user_id=user.id,
        conv_id=conv_id
    )
    logging.debug(f"{user.id} - response: {r}")
    text = r[0].get("text")
    await safe_call(
        callback_query.message.edit_text,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
