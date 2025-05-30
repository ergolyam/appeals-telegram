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
    conversions_view,
    conversions_file_view
)
from appeals.funcs.conversion_admin import (
    conversions_all_list_msg,
    conversions_all_list_cb,
    status_conversion_menu,
    status_conversion_set,
    conversion_remove
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
        pyrogram.handlers.message_handler.MessageHandler(
            conversions_all_list_msg,
            pyrogram.filters.command("admin") &
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
            conversions_all_list_cb,
            pyrogram.filters.regex("^back_to_list$")
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
            status_conversion_menu,
            pyrogram.filters.regex(r"^status_menu:(\d+):(\d+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            status_conversion_set,
            pyrogram.filters.regex(r"^status_set:(\w+):(\d+):(\d+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            conversion_remove,
            pyrogram.filters.regex(r"^remove_conversion:(\d+):(\d+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            conversions_view,
            pyrogram.filters.regex(r"^conv:(\w+):(\d+):(\d+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            conversions_file_view,
            pyrogram.filters.regex(r"^view_file:(\d+):(\d+):(\d+)$")
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
