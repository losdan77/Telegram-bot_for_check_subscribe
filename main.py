from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(mes):
    await mes.answer('Привет! Я бот, который проверит твою подписку на канал.')
    await check_subscribe(mes)


@dp.message_handler()
async def check_subscribe(mes):
    chat_id = '-1001572324800'
    user_channel_status = await bot.get_chat_member(chat_id=chat_id,
                                                    user_id=mes.from_user.id)

    if user_channel_status['status'] != 'left':
        await mes.answer('Вы подписанны на канал, можете получать контент!')
        await send_content(mes)

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Подписаться',
                                              url='https://t.me/fdfgfdgdf'))

        await mes.answer('Для получения контента необходимо подписаться на канал!',
                         reply_markup=markup)
        await mes.answer('После подписки напишите любое сообщение для проверки')


@dp.message_handler()
async def send_content(mes):
    await mes.answer('Контент')


if __name__ == '__main__':
    executor.start_polling(dp)