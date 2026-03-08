import asyncio, random, sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHfCWTjEpn6-XCNh9utMaNGjiv0NxplToQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

LESSONS = {
    "English 🇬🇧": {"hello": "привет", "water": "вода", "bread": "хлеб"},
    "Russian 🇷🇺": {"pri-vet": "hello", "vo-da": "water", "hleb": "bread"}
}

def init_db():
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, language TEXT)')
    conn.commit()
    conn.close()

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(m: types.Message):
    init_db()
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.adjust(1)
    await m.answer(f"Привет, {m.from_user.first_name}!", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def sel_lang(m: types.Message):
    user_id, lang = m.from_user.id, m.text
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)', (user_id, lang))
    conn.commit()
    conn.close()
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Учить ✨"), types.KeyboardButton(text="⬅️ Назад"))
    kb.adjust(1)
    await m.answer(f"Выбран: {lang}", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Учить ✨")
async def quiz(m: types.Message):
    user_id = m.from_user.id
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    if not res: return
    lang = res[0]
    words = LESSONS[lang]
    word = random.choice(list(words.keys()))
    ans = words[word]
    kb = InlineKeyboardBuilder()
    kb.button(text=ans, callback_data="win")
    kb.button(text="В меню", callback_data="exit")
    kb.adjust(1)
    await m.answer(f"Как переводится: {word}?", reply_markup=kb.as_markup())

@dp.callback_query(F.data == "win")
async def win(cb: types.CallbackQuery):
    await cb.message.edit_text("✅ ВЕРНО!")
    await quiz(cb.message)

@dp.callback_query(F.data == "exit")
async def ex(cb: types.CallbackQuery):
    await cb.message.delete()
    await start(cb.message)

async def main(): await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
