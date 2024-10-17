from time import sleep
from telegram import Update
from telegram.ext import ContextTypes

from routines.morning import register_morning_routine

GITHUB_URL = "https://github.com/jacobjwalters/tg-assistant"

async def setup_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guides the user through weather setup"""
    assert update.message is not None
    assert context.user_data is not None

    if "setup_complete" in context.user_data:
        return

    await update.message.reply_text(f"Please send your location to me so I can send you the weather!", parse_mode="HTML")

async def setup_begin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Begins the setup process proper"""
    assert update.message is not None
    assert context.user_data is not None

    if "setup_complete" in context.user_data:
        await update.message.reply_text(f"Welcome back to the setup process!")
        return
    else:
        await update.message.reply_text(f"Great! Let's get started.")

async def setup_complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Completes the setup process"""
    assert update.message is not None
    assert context.user_data is not None

    context.user_data["setup_complete"] = True
    await update.message.reply_text(f"🎉 You're all set up!\nYou can come back here any time to e.g. add another calendar by running /setup once more.")

async def run_setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs the setup process"""
    assert update.message is not None
    assert context.user_data is not None
    assert update.message.from_user is not None

    await update.message.reply_text(f"Hello! I'm going to register you for some automated messages each morning.", parse_mode="HTML")
    await register_morning_routine(update, context)
    sleep(2)
    await setup_weather(update, context)

