import pyrogram.filters
import pyrogram.handlers.message_handler
from appeals.funcs.ping import ping_command


def init_handlers(app):
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            ping_command,
            pyrogram.filters.command("ping") &
                pyrogram.filters.private
        )
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
