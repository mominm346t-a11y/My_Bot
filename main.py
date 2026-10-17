import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "FREE_MULTI_BD" # এখানে তোমার চ্যানেলের username @ ছাড়া বসাও

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Live 24/7"

async def force_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_user.is_bot: return
    try:
        user_id = update.effective_user.id
        check = await context.bot.get_chat_member(f"@{CHANNEL}", user_id)
        if check.status in ['member','administrator','creator']: return

        await update.message.delete()
        btn = [[InlineKeyboardButton("📢 Channel Join করো", url=f"https://t.me/{CHANNEL}")]]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.first_name} ভাই, গ্রুপে লেখার আগে চ্যানেল Join করতে হবে!",
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except: pass

def run_bot():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, force_join))
    app_bot.run_polling()

if __name__ == '__main__':
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
