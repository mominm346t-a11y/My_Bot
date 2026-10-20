import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === এখানে তোমার তথ্য বসাও ===
BOT_TOKEN = os.environ.get("BOT_TOKEN") 8754794998:AAFc3psbdmoBbL-tNT-4VOwKvxKlUT-BBQY
CHANNEL_USERNAME = "@MIM9614"
CHANNEL_LINK = "https://t.me/MIM9614"

# ওয়ার্নিং গোনার জন্য
user_warnings = {}
logging.basicConfig(level=logging.INFO)

async def is_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator', 'owner']
    except:
        return False

async def check_and_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.effective_user is None:
        return
    
    user = update.effective_user
    chat = update.effective_chat

    # অ্যাডমিনদের মেসেজ ডিলিট করবে না
    try:
        member = await context.bot.get_chat_member(chat.id, user.id)
        if member.status in ['administrator', 'creator']:
            return
    except:
        pass

    # চ্যানেলে জয়েন আছে কিনা চেক
    if not await is_joined(update, context):
        try:
            await update.message.delete()
        except:
            pass
        
        keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন / Join Channel", url=CHANNEL_LINK)]]
        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"@{user.username or user.first_name} মেসেজ করার আগে আপনাকে আমাদের চ্যানেলে জয়েন করতে হবে।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except:
            pass
        return

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_joined(update, context):
        keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url=CHANNEL_LINK)]]
        await update.message.reply_text(
            "মেসেজ করার আগে আপনাকে আমাদের চ্যানেলে জয়েন করতে হবে।",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    await update.message.reply_text("Welcome! তুমি জয়েন করেছো।")

# বট চালু
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_and_delete))
app.run_polling()
