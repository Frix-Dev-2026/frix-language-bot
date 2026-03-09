import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ
ABC_GAME = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди")]
LESSONS = {
    "English 🇬🇧": {"hello": "привет", "water": "вода", "bread": "хлеб"},
    "Russian 🇷🇺": {"privet": "hello", "voda": "water", "hleb": "bread"}
}

# 1. ГЛАВНОЕ МЕНЮ
def main_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Курс слов 📚"))
    return kb.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    await m.answer("Выбери режим обучения: 👋", reply_markup=main_kb())

# 2. ИГРА: АЛФАВИТ
@dp.message(F.text == "Алфавит 🔡")
async def quiz_abc(m: types.Message):
    char, sound = random.choice(ABC_GAME)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди"]:
        res = 'w' if s == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{res}_{char}_{sound}"))
    await m.answer(f"Как звучит буква **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

# 3. МЕНЮ: ВЫБОР ЯЗЫКА
@dp.message(F.text == "Курс слов 📚")
async def sel_lang(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    await m.answer("Выбери язык для изучения:", reply_markup=kb.as_markup(resize_keyboard=True))

# 4. ИГРА: СЛОВАРЬ (Срабатывает после выбора языка)
@dp.message(F.text.in_(LESSONS.keys()))
async def start_words(m: types.Message):
    lang = m.text
    word, corr = random.choice(list(LESSONS[lang].items()))
    others = [v for k, v in LESSONS[lang].items() if v != corr]
    opts = random.sample(others, 2) + [corr]
    random.shuffle(opts)
    kb = InlineKeyboardBuilder()
    for o in opts:
        kb.add(types.InlineKeyboardButton(text=o, callback_data=f"ans_{'w' if o == corr else 'l'}_{word}_{corr}_{lang}"))
    await m.answer(f"Курс: {lang}\nКак переводится: **{word}**?", reply_markup=kb.as_markup())

# ОБРАБОТКА КНОПОК
@dp.callback_query(F.data.startswith("abc_"))
async def check_abc(call: types.CallbackQuery):
    d = call.data.split("_")
    msg = f"✅ Верно! [{d[3]}]" if d[1] == 'w' else f"❌ Ошибка! Это [{d[3]}]"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Ещё букву?", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data.startswith("ans_"))
async def check_word(call: types.CallbackQuery):
    d = call.data.split("_")
    status, word, correct, lang = d[1], d[2], d[3], d[4]
    msg = f"✅ Верно! {word} = {correct}" if status == 'w' else f"❌ Ошибка! {word} = {correct}"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text=lang), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer(f"Продолжить курс {lang}?", reply_markup=kb.as_markup(resize_keyboard=True))

async def main(): await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
