from appeals.core.common import Common
from appeals.api.conversion import post_conversion
from appeals.config import logging_config
logging = logging_config.setup_logging(__name__)


async def create_conversion(_, callback_query):
    user = callback_query.from_user
    Common.waiting_for_input[user.id] = {"step": "head"}
    await callback_query.message.reply(
        "Введите <b>заголовок</b> (до 32 символов):"
    )
    await callback_query.answer()


async def create_conversion_text(_, message):
    user = message.from_user
    state = Common.waiting_for_input.get(user.id)

    if not state:
        await message.reply("Введите /start, чтобы начать.")
        return

    if state["step"] == "head":
        head = message.text.strip()

        if len(head) > 32:
            await message.reply(
                "❗️ Заголовок слишком длинный"
                "(максимум 32 символа)."
                "Попробуйте ещё раз."
            )
            return

        state.update({"step": "text", "head": head})
        await message.reply("Теперь введите <b>основное сообщение</b>:")
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

        await message.reply("✅ Сообщение обработано!")
        Common.waiting_for_input.pop(user.id, None)
        return



if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
