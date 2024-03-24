# Телеграм бот для проверки подписки на ваш канал
### Вашему вниманию представляется простой пример кода на языке Python для создания Телеграм бота, который будет проверять пользователей на наличие подписки на определенный канал, для дальнейшей реализации рассылки контента или любой другой функции, с подробным описанием каждого шага. Итоговый код бота будет представден в конце статьи. 
### !Бот обязательно должен быть участником канала, в котором производит проверку подписок!
Рекомендуемые версии Python:
```
Python 3.8 и выше
```
В первую очередь необходимо установить все необходимые зависимости:
```
pip install aiogram==2.25.2
pip install python-dotenv
```
Обращаю внимание на версию библиотеки ```aiogram==2.25.2```, если использовать другую версию некоторые методы могут работать некоректно.

Для корректного хранения ```API_token``` бота в дериктории нашего проекта создаем файл ```.env``` и записываем туда токен бота:
```
TOKEN = 'api токен бота'
```
Теперь непосредственно переходим к написаю бота. В этой же директории создаем файл ```main.py``` и импортируем необходимые библиотеки:
```
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
```
Импортируем api токен бота из файла ```.env```:
```
load_dotenv()
TOKEN = os.getenv('TOKEN')
```
Создаем бота с его api токеном:
```
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
```
Прописываем функцию обработки начала работы с ботом (по команде ```/start```)
```
@dp.message_handler(commands='start')
async def start(mes):
    await mes.answer('Привет! Я бот, который проверит твою подписку на канал.')
    await check_subscribe(mes)
```
После отправки пользователем команды ```/start```, бот отправляет в ответ сообщение ```Привет! Я бот, который проверит твою подписку на канал.```, а так же вызывает функцию ```check_subscribe(mes)``` и передает в нее аргумент ```mes```, который представляет собой ```json``` с полной информацией о полученном сообщении (текст полученного сообщения от пользователя, id пользователя отправившего сообщение и т.д.)

Пропишем вызываемую функцию ```check_subscribe()```:
```
@dp.message_handler()
async def check_subscribe(mes):
    chat_id = '-111111111111'
    user_channel_status = await bot.get_chat_member(chat_id=chat_id,
                                                    user_id=mes.from_user.id)

    if user_channel_status['status'] != 'left':
        await mes.answer('Вы подписанны на канал, можете получать контент!')
        await send_content(mes)

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Подписаться',
                                              url='https://t.me/your_channel'))

        await mes.answer('Для получения контента необходимо подписаться на канал!',
                         reply_markup=markup)
        await mes.answer('После подписки напишите любое сообщение для проверки')
```
```chat_id``` - id канала в котором выполняется проверка подписчиков, получить id канала можно с помощью бота ```@getmyid_bot```, переслав в него любое сообщение из канала. В переменную ```user_channel_status``` с помощью метода ```get_chat_member()``` записываем ```json``` ответ с информацией о статусе подписки пользователя, который обращаеться к боту ```user_id=mes.from_user.id``` на канал ```chat_id=chat_id```. Далее реальзуем конструкцию ```if else``` для проверки подписки пользователя на канал. ```if user_channel_status['status'] != 'left':``` - если значение хранящееся в ключе ```['status']``` неравно ```left```, то информируем пользователя о том, что он подписан на необходимый канал и вызываем функцию ```send_content```, которую реализуем позднее. Во всех других случаях информируем пользователя, о том что ему необходимо подписаться на канал с всплывающей кнопкой для переадресации на канал: ```markup.add(types.InlineKeyboardButton('Подписаться',url='https://t.me/your_channel'))```, затем бот сразу же говорит пользователю, что для повторной проверки подписки, он должен написать любое сообщение боту.

Функция ```send_content()```, выглядит следующим образом:
```
@dp.message_handler()
async def send_content(mes):
    await mes.answer('Контент')
```
Нужна она, для реализации любого функционала, который вы хотите видеть в своем боте, например вы можете сделать рассылку контента, среди пользователей бота с помощью библиотеки [aioschedule](https://pypi.org/project/aioschedule/), пример реализации бота с использованием данной библиотеки вы можете посмотреть [здесь](https://github.com/losdan77/Telegram-bot_for_mailing/tree/main)

Ну и в завершении, обязательно добавить данные строки для работы нашего бота:
```
if __name__ == '__main__':
    executor.start_polling(dp)
```

### Итоговый код:
```
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
    chat_id = '-111111111111'
    user_channel_status = await bot.get_chat_member(chat_id=chat_id,
                                                    user_id=mes.from_user.id)

    if user_channel_status['status'] != 'left':
        await mes.answer('Вы подписанны на канал, можете получать контент!')
        await send_content(mes)

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Подписаться',
                                              url='https://t.me/your_channel'))

        await mes.answer('Для получения контента необходимо подписаться на канал!',
                         reply_markup=markup)
        await mes.answer('После подписки напишите любое сообщение для проверки')


@dp.message_handler()
async def send_content(mes):
    await mes.answer('Контент')


if __name__ == '__main__':
    executor.start_polling(dp)
```
### Вот так довольно просто можно реальзовать бота для проверки подписки на канал.







