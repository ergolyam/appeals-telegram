import asyncio
from appeals.config.config import Config
from appeals.config import logging_config
from appeals.core.common import safe_call
from appeals.funcs.ping import ping_command


async def ping_reset(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/ping reset"
        )
        await ping_command(app, msg)

        out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert out_msg.text == "🏓PONG!\nResp: {'Pong': '0'}", f"Expected '0', got {msg.text!r}"

        logger.info("Test passed! #1 (ping reset)")
    except AssertionError as e:
        logger.error(f"Test failed! #1 (ping reset): {e}")
        raise


async def ping_plus(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/ping plus"
        )
        await ping_command(app, msg)

        out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert out_msg.text == "🏓PONG!\nResp: {'Pong': '1'}", f"Expected '1', got {msg.text!r}"

        logger.info("Test passed! #2 (ping plus)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (ping plus): {e}")
        raise


async def ping_minus(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/ping minus"
        )
        await ping_command(app, msg)

        out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert out_msg.text == "🏓PONG!\nResp: {'Pong': '0'}", f"Expected '0', got {msg.text!r}"

        logger.info("Test passed! #3 (ping minus)")
    except AssertionError as e:
        logger.error(f"Test failed! #3 (ping minus): {e}")
        raise


async def ping_set(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/ping set 42"
        )
        await ping_command(app, msg)

        out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert out_msg.text == "🏓PONG!\nResp: {'Pong': '42'}", f"Expected '42', got {msg.text!r}"

        logger.info("Test passed! #4 (ping set)")
    except AssertionError as e:
        logger.error(f"Test failed! #4 (ping set): {e}")
        raise


async def ping_get(logger, app):
    try:
        msg = await safe_call(
            app.send_message,
            chat_id=Config.test_chat_id,
            text="/ping"
        )
        await ping_command(app, msg)

        out_msg = await app.get_messages(
            chat_id=Config.test_chat_id,
            message_ids=msg.id + 1
        )
        assert out_msg.text == "🏓PONG!\nCount: 42", f"Expected '42', got {msg.text!r}"

        logger.info("Test passed! #5 (ping get)")
    except AssertionError as e:
        logger.error(f"Test failed! #5 (ping get): {e}")
        raise


async def test_ping(app):
    logger = logging_config.setup_logging(__name__)
    async with app:
        await ping_reset(logger, app)
        await asyncio.sleep(1)
        await ping_plus(logger, app)
        await asyncio.sleep(1)
        await ping_minus(logger, app)
        await asyncio.sleep(1)
        await ping_set(logger, app)
        await asyncio.sleep(1)
        await ping_get(logger, app)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
