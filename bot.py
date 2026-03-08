import asyncio
import random
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ПРОВЕРЬ ТОКЕН!
API_TOKEN = '8717727996:AAHfCWTjEpn6-XCNh9utMaNGjiv0NxplToQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

LESSONS = {
    "English 🇬🇧": {
        "hello": ["привет", "[хелоу]"], "water": ["вода", "[уотер]"],
        "bread": ["хлеб", "[брэд]"], "apple": ["яблоко", "[эпл]"],
        "book": ["книга", "[бук]"], "school": ["школа", "[скул]"],
        "friend": ["друг", "[фрэнд]"], "money": ["деньги", "[мани]"],
        "home": ["дом", "[хоум]"], "mother": ["мама", "[мазер]"],
        "father": ["папа", "[фазер]"], "sun": ["солнце", "[сан]"],
        "cat": ["кот", "[кэт]"], "dog": ["собака", "[дог]"],
        "car": ["машина", "[кар]"]
    },
    "Russian 🇷🇺": {
        "privet": ["hello", "[pree-vyet]"], "voda": ["water", "[va-da]"],
        "hleb": ["bread", "[hlyeb]"], "kniga": ["book", "[k-nee-ga]"],
        "mama": ["mother", "[ma-ma]"], "papa": ["father", "[pa-pa]"]
    }
}

ALPHABET_EN = "A [эй], B [би], C [си], D [ди], E [и], F [эф], G [джи], H [эйч], I [ай], J [джей], K [кей], L [эл], M [эм], N [эн], O [оу], P [пи], Q [кью], R [ар], S [эс], T [ти], U [ю], V [ви], W [дабл-ю], X [экс], Y [уай], Z [зед]"
ALPHABET_RU = "А [A], Б [B], В [V], Г [G], Д [D], Е [Ye], Ё [Yo], Ж [Zh], З [Z], И [Ee], Й [Y], К [K], Л [L], М [M], Н [N], О [O], П [P], Р [R], С [S], Т [T], У [U], Ф [F], Х [Kh], Ц [Ts], Ч [Ch], Ш [Sh], Щ [Shch], Ъ [-], Ы [Y], Ь ['], Э [E], Ю [Yu], Я [Ya]"

def init_db():
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, language TEXT)')
    conn.commit()
    conn.close()

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    init_db()
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡"))
    kb.adjust(1)
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\nВыбери обучение:", reply_markup=kb.as_markup(resize_keyboard=True))
    @dp.message(F.text == "Алфавит 🔡")
async def show_alph(m: types.Message):
    await m.answer(f"🔡 **English Alphabet:**\n{ALPHABET_EN}", parse_mode="Markdown")
    await m.answer(f"🔡 **Русский алфавит:**\n{ALPHABET_RU}", parse_mode="Markdown")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_course(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys():
        kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    kb.adjust(1)
    await m.answer("Выбери язык:", reply_markup=kb.as_markup(resize_keyboard=True))

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
    await m.answer(f"Выбран курс: {lang}", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Учить ✨")
async def quiz(m: types.Message):
    user_id = m.from_user.id
    conn = sqlite3.connect('frix_edu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    if not res:
        await m.answer("Сначала выбери
