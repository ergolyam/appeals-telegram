from appeals.api.ping import (
    get_ping,
    post_ping
)


async def ping_command(_, message):
    args = message.text.split()[1:]
    if not args:
        r = await get_ping()
        await message.reply_text(f"🏓PONG!\nCount: {r['Pong']}")
    else:
        try:
            count = int(args[1]) if len(args) > 1 else 0
        except ValueError:
            count = 0
        r = await post_ping(
            args[0],
            count
        )
        await message.reply_text(f"🏓PONG!\nResp: {r}")


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

