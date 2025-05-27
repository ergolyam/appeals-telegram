import asyncio
from appeals.config.config import Config
from appeals.tests.common import (
    DummyCallbackQuery,
    get_callback_data
)
from appeals.config import logging_config

from appeals.funcs.start import (
    start_msg,
    start_cb
)
from appeals.funcs.conversion import (
    create_conversion,
    create_conversion_text,
    conversions_list,
    conversions_view
)


async def create(logger, app):
    try:
        msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)

        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert start_out_msg.text == "Здравствуйте! Выберите действие:", f"Expected 'Здравствуйте! Выберите действие:', got {start_out_msg.text!r}"

        cb_text = "📄 Написать обращение 📄"
        cb_data = get_callback_data(start_out_msg, cb_text)
        assert cb_data is not None, f"Inline-button {cb_text!r} not found"

        fake_query = DummyCallbackQuery(msg=start_out_msg, data=cb_data)
        await create_conversion(app, fake_query)

        head_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 2
        )
        assert head_out_msg.text == "Введите заголовок (до 32 символов):", f"Expected 'Введите заголовок (до 32 символов):', got {head_out_msg.text!r}"

        head_msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="Head Test!"
        )
        await create_conversion_text(app, head_msg)

        text_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=head_msg.id + 1
        )
        assert text_out_msg.text == "Теперь введите основное сообщение:", f"Expected 'Теперь введите основное сообщение:', got {head_out_msg.text!r}"

        text_msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="Text Test!"
        )
        await create_conversion_text(app, text_msg)

        finnaly_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=text_msg.id + 1
        )
        assert finnaly_out_msg.text == "✅ Сообщение обработано!", f"Expected '✅ Сообщение обработано!', got {finnaly_out_msg.text!r}"

        logger.info("Test passed! #1 (create conversion)")
    except AssertionError as e:
        logger.info(f"Test failed! #1 (create conversion): {e}")
        raise


async def view(logger, app):
    try:
        msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)

        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert start_out_msg.text == "Здравствуйте! Выберите действие:", f"Expected 'Здравствуйте! Выберите действие:', got {start_out_msg.text!r}"

        cb_text = "🔍 Текущие обращения 🔎"
        cb_data = get_callback_data(start_out_msg, cb_text)
        assert cb_data is not None, f"Inline-button {cb_text!r} not found"

        fake_query = DummyCallbackQuery(msg=start_out_msg, data=cb_data)
        await conversions_list(app, fake_query)

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
        assert view_out_msg.text == "Text Test!", f"Expected 'Text Test!', got {view_out_msg.text!r}"

        logger.info("Test passed! #2 (view conversion)")
    except AssertionError as e:
        logger.info(f"Test failed! #2 (view conversion): {e}")
        raise


async def ui_create(logger, app):
    cb_text = "📄 Написать обращение 📄"
    back_cb_text = "⬅️ На главную"
    try:
        msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)

        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        cb_data = get_callback_data(start_out_msg, cb_text)
        assert cb_data is not None, f"Inline-button {cb_text!r} not found"
        fake_query = DummyCallbackQuery(msg=start_out_msg, data=cb_data)
        await create_conversion(app, fake_query)

        head_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 2
        )
        back_cb_data = get_callback_data(head_out_msg, back_cb_text)
        assert back_cb_data is not None, f"Inline-button {back_cb_text!r} not found"
        back_fake_query = DummyCallbackQuery(msg=head_out_msg, data=back_cb_data)
        await start_cb(app, back_fake_query)

        start1_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        start1_cb_data = get_callback_data(start1_out_msg, cb_text)
        assert start1_cb_data is not None, f"Inline-button {cb_text!r} not found"
        start1_fake_query = DummyCallbackQuery(msg=start1_out_msg, data=start1_cb_data)
        await create_conversion(app, start1_fake_query)

        head_msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="Head ui Test!"
        )
        await create_conversion_text(app, head_msg)

        text_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=head_msg.id + 1
        )
        back1_cb_data = get_callback_data(text_out_msg, back_cb_text)
        assert back1_cb_data is not None, f"Inline-button {back_cb_text!r} not found"
        back1_fake_query = DummyCallbackQuery(msg=text_out_msg, data=back1_cb_data)
        await start_cb(app, back1_fake_query)

        logger.info("Test passed! #3 (ui create)")
    except AssertionError as e:
        logger.info(f"Test failed! #3 (ui create): {e}")
        raise


async def ui_view(logger, app):
    cb_text = "🔍 Текущие обращения 🔎"
    back_cb_text = "⬅️ На главную"
    try:
        msg = await app.send_message(
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)

        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        cb_data = get_callback_data(start_out_msg, cb_text)
        assert cb_data is not None, f"Inline-button {cb_text!r} not found"
        fake_query = DummyCallbackQuery(msg=start_out_msg, data=cb_data)
        await conversions_list(app, fake_query)

        list_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=start_out_msg.id
        )
        back_cb_data = get_callback_data(list_out_msg, back_cb_text)
        assert back_cb_data is not None, f"Inline-button {back_cb_text!r} not found"
        back_fake_query = DummyCallbackQuery(msg=list_out_msg, data=back_cb_data)
        await start_cb(app, back_fake_query)

        start1_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=list_out_msg.id
        )
        start1_cb_data = get_callback_data(start1_out_msg, cb_text)
        assert start1_cb_data is not None, f"Inline-button {cb_text!r} not found"
        start1_fake_query = DummyCallbackQuery(msg=start1_out_msg, data=start1_cb_data)
        await conversions_list(app, start1_fake_query)

        list1_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=start1_out_msg.id
        )
        list_cb_text = "🆕 Head Test!"
        list_cb_data = get_callback_data(list1_out_msg, list_cb_text)
        assert list_cb_data is not None, f"Inline-button {list_cb_text!r} not found"
        list_fake_query = DummyCallbackQuery(msg=list1_out_msg, data=list_cb_data)
        await conversions_view(app, list_fake_query)

        view_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=list1_out_msg.id
        )
        back1_cb_data = get_callback_data(view_out_msg, back_cb_text)
        assert back1_cb_data is not None, f"Inline-button {back_cb_text!r} not found"
        back1_fake_query = DummyCallbackQuery(msg=view_out_msg, data=back1_cb_data)
        await start_cb(app, back1_fake_query)

        logger.info("Test passed! #4 (ui view)")
    except AssertionError as e:
        logger.info(f"Test failed! #4 (ui view): {e}")
        raise


async def test_conversions(app):
    logger = logging_config.setup_logging(__name__)
    async with app:
        await create(logger, app)
        await asyncio.sleep(1)
        await view(logger, app)
        await asyncio.sleep(1)
        await ui_create(logger, app)
        await asyncio.sleep(1)
        await ui_view(logger, app)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
