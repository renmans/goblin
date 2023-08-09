from os import getenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from api import get_catalog


async def threads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(f"{title}", callback_data=str(title))] for title in get_catalog().keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("/g/ threads:", reply_markup=reply_markup)


app = ApplicationBuilder().token(getenv("GOBLIN_TOKEN")).build()
app.add_handler(CommandHandler("threads", threads))
app.run_polling()
