import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ С КРАСИВЫМ ПРОИЗНОШЕНИЕМ
ABC_GAME = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди"), ("E", "и"), ("F", "эф")]
LESSONS = {
    "English 🇬🇧": {
        "hello": ["привет", "хелоу"], "water": ["вода", "уотер"], 
        "bread": ["хлеб", "брэд"], "apple": ["яблоко", "эпл"]
    },
    "Russian 🇷🇺": {
        "privet": ["hello", "pree-vyet"], "voda": ["water", "va-da"], "hleb": ["bread", "hlyeb"]
    }
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Курс слов 📚"))
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\n\nЯ твой личный учитель. Давай выберем режим обучения ниже:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def quiz_abc(m: types.Message):
    char, sound = random.choice(ABC_GAME)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди", "и", "эф"]:
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{'w' if s == sound else 'l'}_{char}_{sound}"))
    kb.adjust(2)
    await m.answer(f"🔡 **Урок Алфавита**\n\nКак звучит буква: **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_lang(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    await m.answer("📚 **Выбор языка**\n\nКакой курс начнем сегодня?", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def start_words(m: types.Message):
    lang = m.text
    word, data = random.choice(list(LESSONS[lang].items()))
    corr, trans = data[0], data[1]
    others = [v[0] for k, v in LESSONS[lang].items() if v[0] != corr]
    opts = random.sample(others, min(len(others), 2)) + [corr]
    random.shuffle(opts)
    kb = InlineKeyboardBuilder()
    for o in opts: kb.add(types.InlineKeyboardButton(text=o, callback_data=f"ans_{'w' if o == corr else 'l'}_{word}_{corr}_{trans}_{lang}"))
    await m.answer(f"🌍 **Курс: {lang}**\n\nКак переводится слово: **{word}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("abc_"))
async def check_abc(call: types.CallbackQuery):
    _, res, char, sound = call.data.split("_")
    msg = f"✅ **Верно!**\nБуква **{char}** звучит как — **[{sound}]**" if res == 'w' else f"❌ **Ошибка!**\nБуква **{char}** звучит как — **[{sound}]**"
    await call.message.edit_text(msg, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Продолжаем? ✨", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data.startswith("ans_"))
async def check_word(call: types.CallbackQuery):
    _, status, word, corr, trans, lang = call.data.split("_")
    msg = f"✅ **Правильно!**\n**{word}** = **{corr}**\nПроизношение: **[{trans}]**" if status == 'w' else f"❌ **Ошибка!**\n**{word}** — это **{corr}**\nПроизношение: **[{trans}]**"
    await call.message.edit_text(msg, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().a
