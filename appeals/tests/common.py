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


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
