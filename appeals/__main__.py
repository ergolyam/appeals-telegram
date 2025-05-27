import asyncio, signal

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from appeals.config.config import Config
from appeals.config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")


async def main():
    from appeals.core.init import start_bot, stop_bot
    await start_bot()

    loop = asyncio.get_running_loop()

    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    try:
        await stop
    finally:
        await stop_bot()


if __name__ == '__main__':
    if Config.tg_token != 'None':
        asyncio.run(main())
    elif Config.test_session != 'None':
        from appeals.tests.run import run
        asyncio.run(run())
