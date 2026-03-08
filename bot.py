import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Данные для игр
ALPHABET_GAME = [
    ("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди"), ("E", "и"), ("F", "эф"), ("G", "джи"),
    ("H", "эйч"), ("I", "ай"), ("J", "джей"), ("K", "кей"), ("L", "эл"), ("M", "эм"), ("N", "эн")
]

LESSONS = {
    "English 🇬🇧": {"hello": "привет", "water": "вода", "bread": "хлеб", "apple": "яблоко", "book": "книга"},
    "Russian 🇷🇺": {"privet": "hello", "voda": "water", "hleb": "bread", "kniga": "book"}
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start_cmd(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡"))
    kb.adjust(1)
    await m.answer(f"Привет! 👋 Выбери режим обучения:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def start_alpha_quiz(m: types.Message):
    char, sound = random.choice(ALPHABET_GAME)
    others = [s for c, s in ALPHABET_GAME if s != sound]
    options = random.sample(others, 2) + [sound]
    random.shuffle(options)
    
    kb = InlineKeyboardBuilder()
    for opt in options:
        res = 'w' if opt == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=f"abc_{res}_{char}_{sound}"))
    kb.adjust(1)
    await m.answer(f"Как звучит буква **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_lang(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    kb.adjust(1)
    await m.answer("Выбери язык:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def start_word_quiz(m: types.Message):
    lang = m.text
    words = LESSONS[lang]
    word, correct = random.choice(list(words.items()))
    others = [v for k, v in words.items() if v != correct]
    options = random.sample(others, min(len(others), 2)) + [correct]
    random.shuffle(options)
    
    kb = InlineKeyboardBuilder()
    for opt in options:
        res = 'w' if opt == correct else 'l'
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=f"ans_{res}_{word}_{correct}"))
    kb.adjust(1)
    await m.answer(f"Курс: {lang}\nКак переводится: **{word}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("abc_"))
async def check_abc(call: types.CallbackQuery):
    _, status, char, sound = call.data.split("_")
    msg = f"✅ Верно! Буква {char} звучит как [{sound}]" if status == 'w' else f"❌ Ошибка. Буква {char} звучит как [{sound}]"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Ещё букву?", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data.startswith("ans_"))
async def check_word(call: types.CallbackQuery):
    _, status, word, correct = call.data.split("_")
    msg = f"✅ Верно! {word} = {correct}" if status == 'w' else f"❌ Ошибка. {word} = {correct}"
    await call.message.edit_text(msg)
    kb = ReplyKeyboardBuilder()
    kb
