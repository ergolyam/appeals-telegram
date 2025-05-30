from appeals.api.conversion_admin import (
    get_all_conversions,
    set_status_conversion,
    delete_conversion
)
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
from appeals.config import logging_config
logging = logging_config.setup_logging(__name__)


async def conversions_all_list(message):
    if getattr(message, 'data', None) is not None:
        msg_call = message.message.edit_text
    else:
        msg_call = message.reply_text

    user = message.from_user

    passwd = Common.user_admins.get(user.id)
    if passwd is None:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.reply_text("⚠️ Укажите пароль после команды")
            return
        passwd = parts[1]

    r = await get_all_conversions(passwd)

    if r and isinstance(r[0], dict) and "status_code" in r[0]:
        status = r[0]["status_code"]

        if status == 401:
            await safe_call(
                msg_call,
                text="❌ Ошибка авторизации: неверный пароль"
            )
        else:
            await safe_call(
                msg_call,
                text=f"⚠️ Сервер вернул ошибку {status}"
            )
        return

    if Common.user_admins.get(user.id) is None:
        Common.user_admins[user.id] = passwd
        logging.debug(f"{user.id} - logged in! authorized: {Common.user_admins}")

    buttons = []
    for item in r:
        status = ConversionStatus[item["status"]]
        text = f"{status.emoji} {item['head']}"
        user_id = item['user_id']
        buttons.append(
            [InlineKeyboardButton(
                text=text,
                callback_data=f"conv:admin:{user_id}:{item['id']}"
            )]
        )
    await safe_call(
        msg_call,
        text="Все обращения:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def conversions_all_list_msg(_, message):
    await conversions_all_list(message)


async def conversions_all_list_cb(_, callback_query):
    await conversions_all_list(callback_query)


async def status_conversion_menu(_, callback_query):
    data = callback_query.data.split(":")
    user_id = int(data[1])
    conv_id = int(data[2])
    buttons = []
    for status in ConversionStatus:
        button = InlineKeyboardButton(
            text=f"{status.emoji} {status.code}",
            callback_data=f"status_set:{status.code}:{user_id}:{conv_id}",
        )
        buttons.append([button])
    buttons.append([Buttons.back_to_list])
    await safe_call(
        callback_query.message.edit_text,
        text="Выберите статус:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def status_conversion_set(_, callback_query):
    user = callback_query.from_user
    data = callback_query.data.split(":")
    status = str(data[1])
    user_id = int(data[2])
    conv_id = int(data[3])
    passwd = Common.user_admins.get(user.id)
    if passwd:
        r = await set_status_conversion(
            user_id,
            conv_id,
            status,
            passwd
        )
        if r and isinstance(r[0], dict) and "status_code" in r[0]:
            status = r[0]["status_code"]

            if status == 401:
                await safe_call(
                    callback_query.message.edit_text,
                    text="❌ Ошибка авторизации: неверный пароль"
                )
            else:
                await safe_call(
                    callback_query.message.edit_text,
                    text=f"⚠️ Сервер вернул ошибку {status}"
                )
            return
        await safe_call(
            callback_query.message.edit_text,
            text=f"✅ Установлен статус {status}"
        )


async def conversion_remove(_, callback_query):
    user = callback_query.from_user
    data = callback_query.data.split(":")
    user_id = int(data[1])
    conv_id = int(data[2])
    passwd = Common.user_admins.get(user.id)
    if passwd:
        r = await delete_conversion(
            user_id,
            conv_id,
            passwd
        )
        if r[0].get('data') == "unsuccessfully":
            status = r[0]["status_code"]

            if status == 401:
                await safe_call(
                    callback_query.message.edit_text,
                    text="❌ Ошибка авторизации: неверный пароль"
                )
            else:
                await safe_call(
                    callback_query.message.edit_text,
                    text=f"⚠️ Сервер вернул ошибку {status}"
                )
            return
        await safe_call(
            callback_query.message.edit_text,
            text=f"🗑 Обращение удалено"
        )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

