import os
from flask import Flask
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Application
from telegram.ext import MessageHandler
from telegram.ext import filters
from telegram.ext import ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["Amin13247", "Dhaka83", "MIM9614"]

user_warnings = {}
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live!"

async def check_join(update, context):
    if not update.message:
        return
    if not update.effective_user:
        return
    if update.effective_user.is_bot:
        return

    uid = update.effective_user.id
    not_joined = []

    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(
                f"@{ch}", uid)
            if m.status not in [
                'member',
                'administrator',
                'creator'
            ]:
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not not_joined:
        return

    user_warnings[uid] = user_warnings.get(uid, 0) + 1
    w = user_warnings[uid]

    try:
        await update.message.delete()
        name = update.effective_user.first_name
        text = (
            f"মেসেজ করার আগে আপনাকে, {name} "
            "আমাদের চ্যানেলে জয়েন করতে হবে।\n"
            f"(সতর্কবার্তা: {w}/10)"
        )

        keyboard = [
            [InlineKeyboardButton(
                "🔊 Join Channel @Amin13247",
                url="https://t.me/Amin13247")],
            [InlineKeyboardButton(
                "🔊 Join Channel @Dhaka83",
                url="https://t.me/Dhaka83")],
            [InlineKeyboardButton(
                "🔊 Join Channel @MIM9614",
                url="https://t.me/MIM9614")]
        ]

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(e)

def run_bot():
    app_bot = Application.builder().token(
        BOT_TOKEN).build()
    app_bot.add_handler(
        MessageHandler(filters.ALL, check_join))
    app_bot.run_polling()

if __name__ == '__main__':
    import threading
    threading.Thread(
        target=run_bot).start()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 10000))
    )
