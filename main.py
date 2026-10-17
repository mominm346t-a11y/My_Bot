import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["Amin13247", "Dhaka83", "MIM9614"]
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live!"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.is_bot:
        return
    uid = update.effective_user.id
    not_joined=[]
    for ch in CHANNELS:
        try:
            m=await context.bot.get_chat_member(f"@{ch}", uid)
            if m.status not in ['member','administrator','creator']:
                not_joined.append(ch)
        except:
            not_joined.append(ch)
    if not not_joined:
        return
    try:
        await update.message.delete()
    except:
        pass
    btns=[
        [InlineKeyboardButton("Join @Amin13247", url="https://t.me/Amin13247")],
        [InlineKeyboardButton("Join @Dhaka83", url="https://t.me/Dhaka83")],
        [InlineKeyboardButton("Join @MIM9614", url="https://t.me/MIM9614")]
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"⚠️ {update.effective_user.first_name} আগে ৩টা চ্যানেলে Join করো!", reply_markup=InlineKeyboardMarkup(btns))

def start_bot():
    app_bot=Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.ALL, check))
    app_bot.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    threading.Thread(target=start_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
