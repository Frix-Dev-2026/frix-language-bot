import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# ВАШ ТОКЕН УЖЕ ЗДЕСЬ:
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(m: types.Message):
    kb = [[types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await m.answer(f"Привет! Бот запущен! ✅", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
