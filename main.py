from os import getenv
import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv("BOT_TOKEN")

CORRECT_ANSWER = "павук"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_answers = {}


async def send_math_question(chat_id):
    equation = f"{random.randint(1, 10)} + {random.randint(1, 10)}"
    message = await bot.send_message(chat_id, f"Solve the equation: {equation}")
    return message


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def on_new_chat_members(message: types.Message):
    for user in message.new_chat_members:
        question_message = await send_math_question(message.chat.id)
        user_answers[user.id] = {"question_message_id": question_message.message_id, "answered_correctly": False}
        await asyncio.sleep(7)

        try:
            await bot.delete_message(question_message.chat.id, question_message.message_id)
            if not user_answers[user.id]["answered_correctly"]:
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=user.id)
        except Exception as e:
            pass


@dp.message_handler(content_types=[types.ContentType.TEXT])
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_answers and message.text.lower() == CORRECT_ANSWER:
        user_answers[user_id]["answered_correctly"] = True
        await bot.delete_message(message.chat.id, user_answers[user_id]["question_message_id"])
        del user_answers[user_id]


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
