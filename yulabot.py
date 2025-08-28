import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8421520737:AAGzKxtFf91e4lF4nX6MIvnpyB7j1MXdc3I"

# матчим "юл+я+" в любом регистре (и внутри слов)
RE_YULYA = re.compile(r"юл+(я+)", re.IGNORECASE)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:   # пропускаем фото/стикеры/файлы/системные апдейты
        return

    # не отвечаем ботам (включая себя)
    if update.effective_user and update.effective_user.is_bot:
        return

    matches = list(RE_YULYA.finditer(msg.text))
    if not matches:
        return

    ya_len = max(len(m.group(1)) for m in matches)
    reply = "бл" + ("я" * max(1, ya_len))
    await msg.reply_text(reply)

def main():
    logger.info("Starting bot from file: %s", __file__)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()