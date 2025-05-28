import pyrogram.filters
import pyrogram.handlers.message_handler
from appeals.funcs.ping import ping_command
from appeals.funcs.start import (
    start_msg,
    start_cb
)
from appeals.funcs.conversion import (
    create_conversion,
    create_conversion_text,
    skip_files_cb,
    conversions_list,
    conversions_view
)


def init_handlers(app):
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            ping_command,
            pyrogram.filters.command("ping") &
                pyrogram.filters.private
        )
    )
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            start_msg,
            pyrogram.filters.command("start") &
                pyrogram.filters.private
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            start_cb,
            pyrogram.filters.regex("^back_to_menu$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            create_conversion,
            pyrogram.filters.regex("^create_conversion$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            conversions_list,
            pyrogram.filters.regex("^conversions_list$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            conversions_view,
            pyrogram.filters.regex(r"^conv:(\d+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            skip_files_cb,
            pyrogram.filters.regex(r"^skip_files$")
        )
    )
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            create_conversion_text,
            (
                pyrogram.filters.text |
                pyrogram.filters.media
            ) &
                pyrogram.filters.private
        )
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
