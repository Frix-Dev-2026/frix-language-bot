import asyncio, random, sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

API_TOKEN = '8717727996:AAHfCWTjEpn6-XCNh9utMaNGjiv0NxplToQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

LESSONS = {
    "English 🇬🇧": {"hello": "привет", "water": "вода", "bread": "хлеб", "thank you": "спасибо", "friend": "друг", "money": "деньги", "home": "дом"},
    "High Valyrian 🐉": {"rytsas": "привет", "kirisos": "спасибо", "dracarys": "огонь", "azantys": "воин", "zaldrizes": "дракон", "issa": "да", "daor": "нет"},
    "Français 🇫🇷": {"bonjour": "привет", "eau": "вода", "pain": "хлеб", "merci": "спасибо", "ami": "друг", "argent": "деньги", "maison": "дом"},
    "Deutsch 🇩🇪": {"hallo": "привет", "wasser": "вода", "brot": "хлеб", "danke": "спасибо", "freund": "друг", "geld": "деньги", "haus": "дом"},
    "Español 🇪🇸": {"hola": "привет", "agua": "вода", "pan": "хлеб", "gracias": "спасибо", "amigo": "друг", "dinero": "деньги", "casa": "дом"}
}

def init_db():
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, language TEXT)')
    conn.commit()
    conn.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    init_db()
    builder = ReplyKeyboardBuilder()
    for l in LESSONS.keys():
        builder.add(types.KeyboardButton(text=l))
    await message.answer(f"Rytsas, {message.from_user.first_name}! 🌍\nЯ твой учитель.\nВыбери язык:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def select_lang(message: types.Message):
    user_id, lang = message.from_user.id, message.text
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)', (user_id, lang))
    conn.commit()
    conn.close()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Учить слова 📚"))
    await message.answer(f"Отлично! Теперь мы учим {lang}.", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Учить слова 📚")
async def start_test(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    if not res:
        await message.answer("Сначала выбери язык!")
        return
    lang = res[0]
    words = LESSONS[lang]
    word = random.choice(list(words.keys()))
    correct = words[word]
    others = [v for k, v in words.items() if v != correct]
    options = random.sample(others, 2) + [correct]
    random.shuffle(options)
    builder = InlineKeyboardBuilder()
    for opt in options:
        is_cor = "1" if opt == correct else "0"
        builder.button(text=opt, callback_data=f"ans:{is_cor}:{word}")
    builder.adjust(1)
    await message.answer(f"Как переводится: {word.upper()}?", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("ans:"))
async def handle_ans(callback: types.CallbackQuery):
    _, is_cor, word = callback.data.split(":")
    if is_cor == "1":
        await callback.message.edit_text(f"✅ ВЕРНО! {word.upper()}")
    else:
        await callback.message.edit_text(f"❌ ОШИБКА.")
    await start_test(callback.message)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
