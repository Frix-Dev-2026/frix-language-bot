import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ С ПРОИЗНОШЕНИЕМ
ABC_GAME = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди"), ("E", "и"), ("F", "эф")]
LESSONS = {
    "English 🇬🇧": {"hello": ["привет", "[хелоу]"], "water": ["вода", "[уотер]"], "bread": ["хлеб", "[брэд]"], "apple": ["яблоко", "[эпл]"]},
    "Russian 🇷🇺": {"privet": ["hello", "[pree-vyet]"], "voda": ["water", "[va-da]"], "hleb": ["bread", "[hlyeb]"]}
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Курс слов 📚"))
    await m.answer("Выбери режим обучения: 👋", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def quiz_abc(m: types.Message):
    char, sound = random.choice(ABC_GAME)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди", "и", "эф"]:
        res = 'w' if s == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{res}_{char}_{sound}"))
    kb.adjust(2)
    await m.answer(f"Как звучит буква **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_lang(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    await m.answer("Выбери язык:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def start_words(m: types.Message):
    lang = m.text
    word, data = random.choice(list(LESSONS[lang].items()))
    corr, trans = data[0], data[1]
    others = [v[0] for k, v in LESSONS[lang].items() if v[0] != corr]
    opts = random.sample(others, min(len(others), 2)) + [corr]
    random.shuffle(opts)
    kb = InlineKeyboardBuilder()
    # Сокращаем данные для кнопки (max 64 bytes)
    for o in opts: kb.add(types.InlineKeyboardButton(text=o, callback_data=f"ans_{'w' if o == corr else 'l'}_{word[:10]}_{corr[:10]}_{trans[:10]}_{lang[:10]}"))
    await m.answer(f"Курс: {lang}\nКак переводится: **{word}**?", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("abc_"))
async def check_abc(call: types.CallbackQuery):
    d = call.data.split("_")
    msg = f"✅ Верно! {d[2]} звучит как [{d[3]}]" if d[1] == 'w' else f"❌ Ошибка! {d[2]} звучит как [{d[3]}]"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Ещё букву?", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data.startswith("ans_"))
async def check_word(call: types.CallbackQuery):
    d = call.data.split("_")
    status, word, corr, trans, lang = d[1], d[2], d[3], d[4], d[5]
    msg = f"✅ Верно! {word} = {corr} {trans}" if status == 'w' else f"❌ Ошибка! {word} = {corr} {trans}"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text=lang), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer(f"Дальше курс {lang}?", reply_markup=kb.as_markup(resize_keyboard=True))

async def main(): await dp.start
