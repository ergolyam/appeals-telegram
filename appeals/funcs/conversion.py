from io import BytesIO
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
    pin_files_conversion,
    get_conversions,
    get_conversion,
    get_file_conversion
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
    buttons = []
    buttons.append([Buttons.back_to_menu])

    if not state:
        await safe_call(
            message.reply,
            text="Введите /start, чтобы начать."
        )
        return

    if state["step"] == "head":
        head = message.text.strip()

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

    elif state["step"] == "text":
        head = state["head"]
        text = message.text

        r = await post_conversion(
            user_id=user.id,
            head=head,
            text=text
        )
        logging.debug(f"{user.id} - response: {r}")
        state.update({"step": "file", "conv_id": r[0].get('id')})
        buttons.append([Buttons.skip_files])

        await safe_call(
            message.reply,
            text="Пришлите файл для прикрепления или нажмите «Пропустить».",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    elif state["step"] == "file":
        media = message.document or message.photo or message.video
        if not media:
            await safe_call(
                message.reply,
                text="❗️ Пришлите файл или нажмите «Пропустить»."
            )
            return

        if message.document:
            filename = media.file_name or "file"
            mime = media.mime_type or "application/octet-stream"
        elif message.photo:
            filename = "photo.jpg"
            mime = "image/jpeg"
        else:
            filename = "video.mp4"
            mime = "video/mp4"

        file_obj = await message.download(in_memory=True)

        if not isinstance(file_obj, BytesIO):
            file_obj = BytesIO(open(file_obj, "rb").read())

        await pin_files_conversion(
            user.id,
            state["conv_id"],
            filename,
            mime,
            file_obj
        )

        await safe_call(
            message.reply,
            text="✅ Сообщение обработано!"
        )
        Common.waiting_for_input.pop(user.id, None)
        return


async def skip_files_cb(_, callback_query):
    user = callback_query.from_user
    state = Common.waiting_for_input.pop(user.id, None)

    if not state or state.get("step") != "file":
        await callback_query.answer()
        return

    await safe_call(
        callback_query.message.edit_text,
        text="✅ Сообщение обработано!"
    )


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
    files = r[0].get("files")
    if files:
        file_id = files[0].get('id')
        file_name = files[0].get('filename')
        file_type = files[0].get('content_type')
        Common.file_input[user.id] = {"type": file_type, "name": file_name}
        view_files = InlineKeyboardButton(
            text="📁 Вложения 📁",
            callback_data=f"view_file:{conv_id}:{file_id}"
        )
        buttons.append([view_files])
    await safe_call(
        callback_query.message.edit_text,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def conversions_file_view(_, callback_query):
    user = callback_query.from_user
    data = callback_query.data.split(":")
    conv_id = int(data[1])
    file_id = int(data[1])
    state = Common.file_input.get(user.id)
    if state:
        buffer = await get_file_conversion(
            user.id,
            conv_id,
            file_id
        )
        buffer.name = state.get('name')
        await callback_query.message.reply_document(document=buffer)
    await callback_query.answer()


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
