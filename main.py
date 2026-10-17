import os
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["Amin13247", "Dhaka83", "MIM9614"]

print(f"BOT_TOKEN Loaded: {bool(BOT_TOKEN)}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live!"

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.is_bot:
        return
    print(f"MSG from {update.effective_user.id}")
    uid = update.effective_user.id
    not_joined = []
    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(f"@{ch}", uid)
            if m.status not in ['member','administrator','creator']:
                not_joined.append(ch)
        except Exception as e:
            print(f"Error {ch}: {e}")
            not_joined.append(ch)
    if not not_joined:
        return
    try:
        await update.message.delete()
        print("DELETED OK")
    except Exception as e:
        print(f"DELETE FAILED: {e}")
    keyboard = [
        [InlineKeyboardButton("🔊 Join @Amin13247", url="https://t.me/Amin13247")],
        [InlineKeyboardButton("🔊 Join @Dhaka83", url="https://t.me/Dhaka83")],
        [InlineKeyboardButton("🔊 Join @MIM9614", url="https://t.me/MIM9614")]
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"মেসেজ করার আগে আপনাকে, {update.effective_user.first_name} আমাদের চ্যানেলে জয়েন করতে হবে।", reply_markup=InlineKeyboardMarkup(keyboard))

def run_bot():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN NOT FOUND in Render Environment!")
        return
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL, check_join))
    print("Bot Polling Started...")
    app_bot.run_polling()

if __name__ == '__main__':
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
