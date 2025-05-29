import asyncio
from io import BytesIO
from appeals.config.config import Config
from appeals.config import logging_config
from appeals.core.common import (
    safe_call,
    DummyCallbackQuery,
    get_callback_data
)
from appeals.funcs.start import (
    start_msg,
    start_cb
)
from appeals.funcs.conversion import (
    create_conversion,
    create_conversion_text,
    skip_files_cb,
    conversions_list,
    conversions_view,
    conversions_file_view
)


async def create(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)


        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        start_out_text = "Здравствуйте! Выберите действие:"
        assert start_out_msg.text == start_out_text, f"Expected '{start_out_text}', got {start_out_msg.text!r}"
        cb_text = "📄 Написать обращение 📄"
        cb_data = get_callback_data(start_out_msg, cb_text)
        assert cb_data is not None, f"Inline-button {cb_text!r} not found"
        fake_query = DummyCallbackQuery(msg=start_out_msg, data=cb_data)
        await create_conversion(app, fake_query)


        head_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 2
        )
        head_out_text = "Введите заголовок (до 32 символов):"
        assert head_out_msg.text == head_out_text, f"Expected '{head_out_text}', got {head_out_msg.text!r}"
        head_msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="Head Test!"
        )
        await create_conversion_text(app, head_msg)


        text_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=head_msg.id + 1
        )
        text_out_text = "Теперь введите основное сообщение:"
        assert text_out_msg.text == text_out_text, f"Expected '{text_out_text}', got {head_out_msg.text!r}"
        text_msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="Text Test!"
        )
        await create_conversion_text(app, text_msg)


        file_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=text_msg.id + 1
        )
        file_out_text = "Пришлите файл для прикрепления или нажмите «Пропустить»."
        assert file_out_msg.text == file_out_text, f"Expected '{file_out_text}', got {file_out_msg.text!r}"
        file_buffer = BytesIO()
        file_buffer.write(b"Test File")
        file_buffer.seek(0)
        file_buffer.name = "file.txt"
        file_msg = await safe_call(
            app.send_document,
            chat_id=Config.test_chat_id,
            document=file_buffer
        )
        await create_conversion_text(app, file_msg)


        finnaly_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=file_msg.id + 1
        )
        finnaly_out_text = "✅ Сообщение обработано!"
        assert finnaly_out_msg.text == finnaly_out_text, f"Expected '{finnaly_out_text}', got {finnaly_out_msg.text!r}"


        logger.info("Test passed! #1 (create conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #1 (create conversion): {e}")
        raise


async def view(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/start"
        )
        await start_msg(app, msg)


        start_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        start_out_text = "Здравствуйте! Выберите действие:"
        assert start_out_msg.text == start_out_text, f"Expected '{start_out_text}', got {start_out_msg.text!r}"
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


        logger.info("Test passed! #2 (view conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (view conversion): {e}")
        raise


async def ui_create(logger, app):
    cb_text = "📄 Написать обращение 📄"
    back_cb_text = "⬅️ На главную"
    try:
        msg = await safe_call(
            app.send_message,
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


        head_msg = await safe_call(
            app.send_message,
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


        start2_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        start2_cb_data = get_callback_data(start2_out_msg, cb_text)
        assert start2_cb_data is not None, f"Inline-button {cb_text!r} not found"
        start2_fake_query = DummyCallbackQuery(msg=start2_out_msg, data=start2_cb_data)
        await create_conversion(app, start2_fake_query)


        head1_msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="Head ui Test!"
        )
        await create_conversion_text(app, head1_msg)


        text_msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="Text ui Test!"
        )
        await create_conversion_text(app, text_msg)


        text_out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=text_msg.id + 1
        )
        skip_cb_text = "🚫 Пропустить 🚫"
        skip_cb_data = get_callback_data(text_out_msg, skip_cb_text)
        assert skip_cb_data is not None, f"Inline-button {skip_cb_text!r} not found"
        skip_fake_query = DummyCallbackQuery(msg=text_out_msg, data=skip_cb_data)
        await skip_files_cb(app, skip_fake_query)


        logger.info("Test passed! #3 (ui create)")
    except AssertionError as e:
        logger.error(f"Test failed! #3 (ui create): {e}")
        raise


async def ui_view(logger, app):
    cb_text = "🔍 Текущие обращения 🔎"
    back_cb_text = "⬅️ На главную"
    try:
        msg = await safe_call(
            app.send_message,
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
        logger.error(f"Test failed! #4 (ui view): {e}")
        raise


async def test_conversions(app):
    logger = logging_config.setup_logging(__name__)
    async with app:
        await create(logger, app)
        await view(logger, app)
        await ui_create(logger, app)
        await ui_view(logger, app)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
