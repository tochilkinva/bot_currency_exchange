"""
Telegram бот для получения курсов валют с сайта www.cbr.ru.

Отправьте сообщение в формате:

Формат: сумма, текущая валюта, необходимая валюта
10000,0 RUB USD

Формат: сумма, текущая валюта, необходимая валюта, курс(USD/RUB=77.9999)
10000 RUB USD 77.9999

Формат: сумма, текущая валюта, необходимая валюта, обратный курс(RUB/USD=1/76.82071)
10000.0 USD RUB /76.82071
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from currency_converter import run, get_codes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)


HELP_MSG = """
Telegram бот для получения курсов валют.
Отправьте сообщение в формате:

Формат: сумма, текущая валюта, необходимая валюта
10000,0 RUB USD

Формат: сумма, текущая валюта, необходимая валюта, курс(USD/RUB=77.9999)
10000 RUB usd 77,9999

Формат: сумма, текущая валюта, необходимая валюта, обратный курс(RUB/USD=1/76.82071)
10000.0 Usd Rub /76.82071

Команда выводит список доступных курсов с кодами
/codes
"""


# Хэндлер на команду /start , /help
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(HELP_MSG)


# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    """
    Обработчик команды /test
    """
    await message.answer("Test")


# Хэндлер на команду /codes
@dp.message_handler(commands="codes")
async def cmd_codes(message: types.Message):
    """
    Обработчик команды /codes
    """
    codes = get_codes()
    await message.answer(codes)


# Хэндлер на получение текста
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def cmd_text(message: types.Message):
    """
    Обработчик на получение текста
    """
    try:
        result_text = run(message.text)
    except Exception as exc:
        result_text = f"Произошла ошибка: {exc}"

    await message.reply(result_text)


if __name__ == "__main__":
    # Запуск бота
    print("Запуск бота")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
