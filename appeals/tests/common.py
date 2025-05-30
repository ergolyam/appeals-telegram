class DummyCallbackQuery:
    def __init__(self, *, msg, data):
        self.id = "local-test"
        self.from_user = msg.from_user
        self.chat_instance = "dummy"
        self.message = msg
        self.data = data

    async def answer(self, *args, **kwargs):
        return True

def get_callback_data(
        message,
        target_text: str
):
    kb = getattr(
        message.reply_markup,
        "inline_keyboard",
        None
    )
    if kb is None:
        return None

    for row in kb:
        for button in row:
            if button.text == target_text:
                return button.callback_data


async def clicker(app, func, chat_id, msg_id, cb_text):
    msg = await app.get_messages(
        chat_id=chat_id,
        message_ids=msg_id
    )
    cb_data = get_callback_data(msg, cb_text)
    assert cb_data is not None, f"Inline-button {cb_text!r} not found"
    fake_query = DummyCallbackQuery(msg=msg, data=cb_data)
    await func(app, fake_query)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
