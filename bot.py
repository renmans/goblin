from os import getenv
from random import choice
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from api import get_catalog


async def threads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    catalog = get_catalog()
    keyboard = [[InlineKeyboardButton(f"{title}", callback_data=str(title))] for title in catalog.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    img = choice([v['media'] for _, v in catalog.items() if v['media']])
    await update.message.reply_photo(img, reply_markup=reply_markup)


app = ApplicationBuilder().token(getenv("GOBLIN_TOKEN")).build()
app.add_handler(CommandHandler("threads", threads))
app.run_polling()
