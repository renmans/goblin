from os import getenv
from random import choice
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from api import get_catalog

# The Kostil
CURRENT_CATALOG = {}


async def threads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global CURRENT_CATALOG
    catalog = get_catalog()
    CURRENT_CATALOG = catalog
    keyboard = [[InlineKeyboardButton(f"{title}", callback_data=str(content['id']))] for title, content in catalog.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    img = choice([v['media'] for _, v in catalog.items() if v['media']])
    await update.message.reply_photo(img, reply_markup=reply_markup)


async def thread(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    catalog = CURRENT_CATALOG
    query = update.callback_query
    await query.answer()
    for _, content in catalog.items():
        if str(content['id']) == query.data:
            if content['ext'] in ['.jpeg', '.jpg', '.png', '.webp']:    
                await query.message.reply_photo(content["media"], caption=content['content'], parse_mode='HTML')
            # telegram don't support .webm
            elif content['ext'] == '.mp4':
                await query.message.reply_video(content["media"], caption=content['content'], parse_mode='HTML')
            else:
                await query.message.reply_html(content['content'])


app = ApplicationBuilder().token(getenv("GOBLIN_TOKEN")).build()
app.add_handler(CommandHandler("threads", threads))
app.add_handler(CallbackQueryHandler(thread))
app.run_polling(allowed_updates=Update.ALL_TYPES)
