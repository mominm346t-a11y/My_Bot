from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"
def run(): app.run(host='0.0.0.0', port=10000)
Thread(target=run).start()

import asyncio
import os
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNEL_ID") # এখানে , দিয়ে দিয়ে চ্যানেল দিবে

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# কমা দিয়ে আলাদা করা
CHANNEL_LIST = [ch.strip() for ch in CHANNELS.split(",") if ch.strip()]

@dp.message()
async def check_join(message: types.Message):
    try:
        for CHANNEL_ID in CHANNEL_LIST:
            member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
            if member.status in ['left', 'kicked']:
                await message.delete()
                # সব চ্যানেলের লিস্ট দেখাবে
                all_channels = "\n".join(CHANNEL_LIST)
                msg = await message.answer(f"@{message.from_user.username or message.from_user.first_name} আগে জয়েন করুন 👇\n{all_channels}\nতারপর মেসেজ দিন।")
                await asyncio.sleep(15)
                await msg.delete()
                return
    except Exception as e:
        print(e)
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
