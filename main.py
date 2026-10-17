import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS_RAW = os.getenv("CHANNELS", "MIM9614,Amin13247,Dhaka83")
CHANNELS = [c.strip().replace("@","") for c in CHANNELS_RAW.replace("[","").replace("]","").replace('"',"").replace("'","").split(",") if c.strip()]

print(f"BOT_TOKEN OK? {bool(BOT_TOKEN)} - Channels: {CHANNELS}", flush=True)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.is_bot:
        return
    uid = update.effective_user.id
    chat_id = update.effective_chat.id
    print(f"Msg from {uid}", flush=True)
    not_joined = []
    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(f"@{ch}", uid)
            if m.status not in ['member','administrator','creator']:
                not_joined.append(ch)
        except:
            not_joined.append(ch)
    if not not_joined:
        return
    try:
        await update.message.delete()
        print("DELETED", flush=True)
    except Exception as e:
        print(f"DELETE FAILED: {e}", flush=True)
        return
    btns = [[InlineKeyboardButton(f"Join @{c}", url=f"https://t.me/{c}")] for c in CHANNELS]
    await context.bot.send_message(chat_id, f"⚠️ Join {', '.join(['@'+c for c in CHANNELS])} first!", reply_markup=InlineKeyboardMarkup(btns))

def run_bot():
    print("Starting Bot Polling...", flush=True)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, check_join))
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
