from calendar import c
import logging
from math import nan
from typing import Tuple

from telegram import Update
from telegram.ext import ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert context.user_data is not None

    if "user_id" not in context.user_data:
        await update.message.reply_text("Please run /start to set up your account.")
        logging.info(f"new uid: {context.user_data['user_id']}")
        return
    else:
        await update.message.reply_text("I didn't get that! Please run one of the supported commands.")

async def get_loc(context: ContextTypes.DEFAULT_TYPE) -> Tuple[float, float]:
    assert context.user_data is not None

    # TODO: track location via external DB

    if "lat" in context.user_data and "lon" in context.user_data:
        lat = context.user_data["lat"]
        lon = context.user_data["lon"]
        return (lat, lon)

    else:
        logging.info("No user-provided information found.")
        await context.bot.send_message(chat_id=context.user_data["user_id"], text="🗺️ Please send me your location and try again.")
        return (nan, nan)

async def set_loc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert context.user_data is not None
    assert update.message is not None
    assert update.message.location is not None

    context.user_data["lat"] = update.message.location.latitude
    context.user_data["lon"] = update.message.location.longitude
    await update.message.reply_text(f"Got your location: {context.user_data['lat']}, {context.user_data['lon']}")

