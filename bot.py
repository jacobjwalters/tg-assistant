#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""This example showcases how PTBs "arbitrary callback data" feature can be used.

For detailed info on arbitrary callback data, see the wiki page at
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Arbitrary-callback_data

Note:
To use arbitrary callback data, you must install PTB via
`pip install "python-telegram-bot[callback-data]"`
"""
import logging
from math import nan
from os import environ
from typing import Tuple

from telegram import __version__ as TG_VER
from telegram import ReplyKeyboardMarkup

from utils import handle_message, set_loc

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
    filters,
    MessageHandler,
)

import datetime
import pytz

from routines.morning import * #morning, add_email_account, start_morning
from routines.setup import run_setup

from data_sources.weather import today_forecast

import utils

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None
    assert update.message.from_user is not None
    assert context.user_data is not None

    context.user_data["user_id"] = update.message.from_user.id

    await update.message.reply_text("Hello! I'm a personal assistant bot. I'll do my best to help you with your day-to-day life! Run /setup to begin :D")

async def run_morning_routine(context: ContextTypes.DEFAULT_TYPE) -> None:
    ids = context.bot_data["morning_routine_ids"] if "morning_routine_ids" in context.bot_data else []
    for id in ids:
        await start_morning(id, context)

async def reset_setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert context.user_data is not None

    context.user_data.pop("setup_complete")
    await update.message.reply_text("Reset setup.")

def main() -> None:
    """Run the bot."""
    persistence = PicklePersistence(filepath="tg_assistant_persistence.pickle")

    application = (
        Application.builder()
        .token(environ["TG_TOKEN"])
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setup", run_setup))
    application.add_handler(CommandHandler("reset_setup", reset_setup))
    application.add_handler(CommandHandler("weather", lambda _, c: today_forecast(c)))
    application.add_handler(MessageHandler(filters.LOCATION, set_loc))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Morning message
    job_queue = application.job_queue
    assert job_queue is not None
    #job_morning   = job_queue.run_daily(run_morning_routine, time=datetime.time(hour=9,  minute=0, second=0, tzinfo=pytz.timezone("Europe/London")))
    job_morning   = job_queue.run_daily(today_forecast, time=datetime.time(hour=9,  minute=0, second=0, tzinfo=pytz.timezone("Europe/London")))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
