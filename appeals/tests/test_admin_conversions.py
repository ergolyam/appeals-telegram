from appeals.config.config import Config
from appeals.config import logging_config
from appeals.core.common import (
    safe_call,
    DummyCallbackQuery,
    get_callback_data
)
from appeals.funcs.conversion_admin import (
    conversions_all_list_msg,
    conversions_all_list_cb
)

from appeals.funcs.conversion import (
    conversions_view,
    conversions_file_view
)


async def view(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/admin admin"
        )
        await conversions_all_list_msg(app, msg)


        list_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        list_cb_text = "🆕 Head Test!"
        list_cb_data = get_callback_data(list_out_msg, list_cb_text)
        assert list_cb_data is not None, f"Inline-button {list_cb_text!r} not found"
        list_fake_query = DummyCallbackQuery(msg=list_out_msg, data=list_cb_data)
        await conversions_view(app, list_fake_query)


        view_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        view_out_text = "Text Test!"
        assert view_out_msg.text == view_out_text, f"Expected '{view_out_text}', got {view_out_msg.text!r}"
        view_cb_text = "📁 Вложения 📁"
        view_cb_data = get_callback_data(view_out_msg, view_cb_text)
        assert view_cb_data is not None, f"Inline-button {view_cb_text!r} not found"
        view_fake_query = DummyCallbackQuery(msg=view_out_msg, data=view_cb_data)
        await conversions_file_view(app, view_fake_query)


        file_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=view_out_msg.id + 1
        )
        file_media = await app.download_media(file_out_msg, in_memory=True)
        file_media.seek(0)
        file_data = file_media.read().decode("utf-8")
        file_out_text = "Test File"
        assert file_data == file_out_text, f"Expected '{file_out_text}', got {file_data!r}"


        logger.info("Test passed! #1 (admin view conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #1 (admin view conversion): {e}")
        raise


async def ui_view(logger, app):
    back_cb_text = "⬅️ На главную"
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/admin"
        )
        await conversions_all_list_msg(app, msg)


        list_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        list_cb_text = "🆕 Head Test!"
        list_cb_data = get_callback_data(list_out_msg, list_cb_text)
        assert list_cb_data is not None, f"Inline-button {list_cb_text!r} not found"
        back_fake_query = DummyCallbackQuery(msg=list_out_msg, data=list_cb_data)
        await conversions_view(app, back_fake_query)


        view_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=list_out_msg.id
        )
        back_cb_data = get_callback_data(view_out_msg, back_cb_text)
        assert back_cb_data is not None, f"Inline-button {back_cb_text!r} not found"
        back_fake_query = DummyCallbackQuery(msg=view_out_msg, data=back_cb_data)
        await conversions_all_list_cb(app, back_fake_query)


        logger.info("Test passed! #2 (admin ui view)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (admin ui view): {e}")
        raise


async def test_admin_conversions(app):
    logger = logging_config.setup_logging(__name__)
    async with app:
        await view(logger, app)
        await ui_view(logger, app)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

