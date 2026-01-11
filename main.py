import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from boltiotai import openai
from example import example

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Start Flask app in background
example()


@dp.message(CommandStart(['start', 'help']))
async def welcome(message: types.Message):
    await message.reply(
        "Hello!\n"
        "I am a GPT-powered Telegram bot.\n"
        "Ask me anything"
    )

@dp.message()
async def gpt(message: types.Message):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.text}
        ]

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        await message.reply(
            response["choices"][0]["message"]["content"]
        )

    except Exception as e:
        await message.reply("Error while processing your request.")
        print("ERROR:", e)

#START BOT 

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())