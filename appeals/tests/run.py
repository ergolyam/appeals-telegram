import logging as logging_base
from pyrogram.client import Client
from appeals.config import logging_config
from appeals.config.config import Config

from appeals.tests.test_ping import test_ping
from appeals.tests.test_conversions import test_conversions
from appeals.tests.test_admin_conversions import test_admin_conversions


async def run():
    logging = logging_config.setup_logging(__name__)
    test_app = Client(
        name="dummy",
        api_id=Config.tg_id,
        api_hash=Config.tg_hash,
        session_string=Config.test_session,
        in_memory=True
    )

    error_count = 0
    warning_count = 0
    passed_count = 0

    class TestLoggingHandler(logging_base.Handler):
        def emit(self, record):
            nonlocal error_count, warning_count, passed_count
            log_message = self.format(record)
            if 'Test passed!' in log_message:
                passed_count += 1
            elif 'Test failed!' in log_message or 'An error occurred' in log_message:
                error_count += 1
            elif 'Warning' in log_message or 'Expected' in log_message:
                warning_count += 1

    test_logging_handler = TestLoggingHandler()
    logging_base.getLogger().addHandler(test_logging_handler)

    try:
        logging.info(f'Start tests...')
        await test_ping(test_app)
        await test_conversions(test_app)
        await test_admin_conversions(test_app)
    finally:
        logging.info(f'All tests completed! [Errors: {error_count}, Warnings: {warning_count}, Passed: {passed_count}]')


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

