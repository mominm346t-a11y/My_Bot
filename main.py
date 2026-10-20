import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# === এখানে তোমার তথ্য বসাও ===
BOT_TOKEN 8615086366:AAGgJvdjT6F_BBnMAMBekOA2ub7HsPeTuzE
CHANNEL_USERNAME = "@MIM9614"  # তোমার চ্যানেল
CHANNEL_LINK = "https://t.me/MIM9614"

# ওয়ার্নিং গোনার জন্য
user_warnings = {}

# লগ
logging.basicConfig(level=logging.INFO)

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

    # চ্যানেলে জয়েন আছে কিনা চেক
    try:
        ch_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
        if ch_member.status in ['member', 'administrator', 'creator']:
            return # জয়েন আছে, কিছু করবে না
    except:
        # জয়েন নাই
        pass

    # জয়েন নাই -> মেসেজ ডিলিট
    try:
        await update.message.delete()
    except:
        pass

    # ওয়ার্নিং বাড়াও
    warnings = user_warnings.get(user.id, 0) + 1
    user_warnings[user.id] = warnings

    if warnings >= 10:
        try:
            await context.bot.ban_chat_member(chat.id, user.id)
            await context.bot.send_message(chat.id, f"{user.first_name} কে 10 বার সতর্ক করার পর ব্যান করা হলো।")
            user_warnings[user.id] = 0
        except:
            pass
        return

    # তোমার স্ক্রিনশটের মতো মেসেজ + বাটন
    text = f"মেসেজ করার ,🙈 نينو للجادين (النبذة)\nআগে আপনাকে আমাদের চ্যানেলে জয়েন করতে হবে। (সতর্কবার্তা: {warnings}/10)"

    keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন / Join Channel", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_and_delete))
print("Bot is running...")
app.run_polling()
