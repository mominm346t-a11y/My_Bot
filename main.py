from flask import Flask
from threading import Thread
import os, re, asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Flask - Render কে বাঁচিয়ে রাখার জন্য
app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"
def run(): app.run(host='0.0.0.0', port=10000)
Thread(target=run).start()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
LINK_PATTERN = r"t\.me|telegram\.me|telegram\.dog"

async def delete_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        if re.search(LINK_PATTERN, update.message.text, re.IGNORECASE):
            try:
                await update.message.delete()
                print(f"Deleted: {update.message.text}")
            except Exception as e:
                print(f"Delete failed: {e}")

async def main():
    print("Starting Bot...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_link))
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
