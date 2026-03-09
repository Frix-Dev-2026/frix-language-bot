import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ПРОВЕРЬ ТВОЙ ТОКЕН: 
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ
ABC = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди")]
WORDS = {"English 🇬🇧": {"hello": ["привет", "хелоу"], "water": ["вода", "уотер"]}}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Курс слов 📚"))
    await m.answer(f"Привет! Выбери обучение:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def q_abc(m: types.Message):
    char, sound = random.choice(ABC)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди"]:
        res = 'w' if s == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{res}_{char}_{sound}"))
    await m.answer(f"Как звучит: **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("abc_"))
async def c_abc(call: types.CallbackQuery):
    d = call.data.split("_")
    m = f"✅ **Верно!** [{d[3]}]" if d[1] == 'w' else f"❌ **Ошибка!** Это [{d[3]}]"
    await call.message.edit_text(m, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Дальше?", reply_markup=kb.as_markup(resize_keyboard=True))

async def main(): await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
