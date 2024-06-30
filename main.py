from os import getenv
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = int(getenv("BOT_TOKEN"))

CORRECT_ANSWER = "set correct answer here"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_answers = {}


@dp.message_handler(commands=['set'])
async def set_correct_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id == AUTHORIZED_USER_ID:
        try:
            global CORRECT_ANSWER
            _, new_answer = message.text.split(' ', 1)
            CORRECT_ANSWER = new_answer.strip()
            await message.reply(f"The correct answer has been updated to: {CORRECT_ANSWER}")
        except ValueError:
            await message.reply("Please provide a new answer like this: /set <answer>")


@dp.message_handler(commands=['check'])
async def check_bot(message: types.Message):
    user_id = message.from_user.id
    if user_id == AUTHORIZED_USER_ID:
        await message.reply(f"I'm fine, I'm working!")


async def send_math_question(chat_id):
    equation = f"{random.randint(1, 10)} + {random.randint(1, 10)}"
    message = await bot.send_message(chat_id, f"Solve the equation: {equation}")
    return message


@dp.message_handler(content_types=['new_chat_members'])
async def on_new_chat_members(message: types.Message):
    for user in message.new_chat_members:
        question_message = await send_math_question(message.chat.id)
        user_answers[user.id] = {"question_message_id": question_message.message_id, "answered_correctly": False}
        await asyncio.sleep(7)

        try:
            await bot.delete_message(question_message.chat.id, question_message.message_id)
            if not user_answers[user.id]["answered_correctly"]:
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=user.id)
                print(message.chat.id, user.id)
                try:
                    await bot.unban_chat_member(message.chat.id, user.id)
                except Exception as e:
                    pass
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
