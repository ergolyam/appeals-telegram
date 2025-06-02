# appeals-telegram
An asynchronous Telegram bot for filing and tracking citizen appeals (service requests) through chat. The bot posts every appeal to a separate FastAPI service – see **[appeals‑backend](https://github.com/grisha765/appeals-backend)** – and lets users follow its life‑cycle without leaving Telegram. Built for learning purposes and needs further refinement, but it can be used now: Pyrogram, coloured console logging, dotenv configuration and self‑contained integration tests.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Environment `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Environment `venv` using `uv`.

```shell
git clone https://github.com/grisha765/appeals-telegram.git
cd appeals-telegram
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv sync
```

## Usage

### Deploy

- Run the bot:
    ```bash
    TG_TOKEN="telegram_bot_token" .venv/bin/python appeals
    ```
    - Make sure the sibling **appeals-backend** service is running and reachable at the `API_ADDRESS` configured below.

## Environment Variables

The following environment variables control the startup of the project:

| Variable       | Values                              | Description                                                             |
| -------------- | ----------------------------------- | ----------------------------------------------------------------------- |
| `LOG_LEVEL`    | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Logging verbosity                                                       |
| `TG_ID`        | *integer*                           | Telegram API ID from [https://my.telegram.org](https://my.telegram.org) |
| `TG_HASH`      | *string*                            | Telegram API hash                                                       |
| `TG_TOKEN`     | *string*                            | Bot token issued by @BotFather                                          |
| `API_ADDRESS`  | `http://127.0.0.1:8000`, custom URL | Base URL of the REST backend                                            |
| `TEST_SESSION` | *string* or empty                   | Session string for the test account (integration)                       |
| `TEST_CHAT_ID` | *integer*                           | Chat ID used by the test‑suite                                          |

## Features

- Async Telegram bot powered by Pyrogram.
- Works with the fully‑async appeals-backend REST API.
- Supports text + media attachments and multi‑step status flow.
- Role‑based command set for citizens and administrators.
- Colourised structured logging to console and daily log files.
- 100 % type‑hinted codebase with built‑in integration tests.

