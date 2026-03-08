import asyncio, random, sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHfCWTjEpn6-XCNh9utMaNGjiv0NxplToQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

LESSONS = {
    "English for Russians 🇬🇧/🇷🇺": {
        "hello": ["привет", "[хелоу]"], "water": ["вода", "[уотер]"], "bread": ["хлеб", "[брэд]"],
        "friend": ["друг", "[фрэнд]"], "money": ["деньги", "[мани]"]
    },
    "Русский для Англичан 🇷🇺/🇬🇧": {
        "привет": ["hello", "[pree-vyet]"], "вода": ["water", "[va-da]"], "хлеб": ["bread", "[hlyeb]"]
    }
}

def init_db():
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, language TEXT)')
    conn.commit()
    conn.close()

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def cmd_start(message: types.Message):
    init_db()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡"))
    builder.adjust(1)
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def show_alph(message: types.Message):
    await message.answer("ABC... / АБВ...")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_course(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): builder.add(types.KeyboardButton(text=l))
    builder.adjust(1)
    await message.answer("Выбери курс:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def sel_lang(message: types.Message):
    user_id, lang = message.from_user.id, message.text
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)', (user_id, lang))
    conn.commit()
    conn.close()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Учить ✨"), types.KeyboardButton(text="⬅️ Назад"))
    builder.adjust(1)
    await message.answer(f"Курс: {lang}", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Учить ✨")
async def start_test(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    if not res: return
    lang = res[0]
    words = LESSONS[lang]
    word = random.choice(list(words.keys()))
    corr = words[word][0]
    builder = InlineKeyboardBuilder()
    builder.button(text=corr, callback_data="win")
    builder.button(text="Выход", callback_data="exit")
    builder.adjust(1)
    await message.answer(f"Как переводится: {word}?", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "win")
async def win(cb: types.CallbackQuery):
    await cb.message.edit_text("✅ ВЕРНО!")
    await start_test(cb.message)

@dp.callback_query(F.data == "exit")
async def ex(cb: types.CallbackQuery):
    await cb.message.delete()
    await cmd_start(
