import os, threading, asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN Loaded: {bool(BOT_TOKEN)}")

CHANNELS = ["Amin13247", "Dhaka83", "MIM9614"]
user_warnings = {}
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live!"

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.is_bot:
        return
    uid = update.effective_user.id
    print(f"MSG from {uid}: {update.message.text}")
    
    not_joined = []
    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(f"@{ch}", uid)
            if m.status not in ['member','administrator','creator']:
                not_joined.append(ch)
        except Exception as e:
            print(f"Check fail {ch}: {e}")
            not_joined.append(ch)
    
    if not not_joined:
        return

    try:
        await update.message.delete()
        print("DELETED SUCCESS")
    except Exception as e:
        print(f"DELETE FAILED - Bot is not Admin in group: {e}")

    keyboard = [
        [InlineKeyboardButton("Join @Amin13247", url="https://t.me/Amin13247")],
        [InlineKeyboardButton("Join @Dhaka83", url="https://t.me/Dhaka83")],
        [InlineKeyboardButton("Join @MIM9614", url="https://t.me/MIM9614")]
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"⚠️ {update.effective_user.first_name} আগে ৩টা চ্যানেলে Join করো।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def run_bot():
    try:
        print("Starting Bot Polling...")
        # This will clear old polling
        app_bot = Application.builder().token(BOT_TOKEN).build()
        app_bot.add_handler(MessageHandler(filters.ALL, check_join))
        print("Bot Polling Started - OK")
        app_bot.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"BOT CRASHED: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
