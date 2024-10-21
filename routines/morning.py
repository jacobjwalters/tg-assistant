from telegram import Update
from telegram.ext import ContextTypes

from data_sources.weather import today_forecast


async def register_morning_routine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None

    ids = context.bot_data["morning_routine_ids"] if "morning_routine_ids" in context.bot_data else []
    ids.append(update.message.chat_id)
    context.bot_data["morning_routine_ids"] = ids
    await update.message.reply_text(f"Registered morning routine for {update.message.chat_id}.")


async def start_morning(id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Walks the user through leaving bed"""

    #await context.bot.send_message(chat_id=id, text="Good morning! I hope you slept well.\nAre you ready to start your day?")
    await morning(context)


async def morning(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs the morning routine"""
    assert context.user_data is not None

    await today_forecast(context)

