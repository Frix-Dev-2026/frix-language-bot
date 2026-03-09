import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ПРОВЕРЬ ТОКЕН: 
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ
ABC = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди")]
WORDS = {
    "English 🇬🇧": {"hello": ["привет", "хелоу"], "water": ["вода", "уотер"]},
    "Russian 🇷🇺": {"privet": ["hello", "pree-vyet"], "kniga": ["book", "k-nee-ga"]}
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Курс слов 📚"))
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\nЯ твой учитель. Выбери режим:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def q_abc(m: types.Message):
    char, sound = random.choice(ABC)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди"]:
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{'w' if s == sound else 'l'}_{char}_{sound}"))
    await m.answer(f"🧪 **Алфавит**\nКак звучит буква: **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_l(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in WORDS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    await m.answer("🌍 **Выбор языка**:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(WORDS.keys()))
async def start_w(m: types.Message):
    l = m.text
    w, d = random.choice(list(WORDS[l].items()))
    c, t = d[0], d[1]
    opts = random.sample([v[0] for v in WORDS[l].values() if v[0] != c], 1) + [c]
    random.shuffle(opts)
    kb = InlineKeyboardBuilder()
    for o in opts: kb.add(types.InlineKeyboardButton(text=o, callback_data=f"ans_{'w' if o == c else 'l'}_{w}_{c}_{t}_{l}"))
    await m.answer(f"🌍 **Курс: {l}**\nКак переводится: **{w}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("abc_"))
async def c_abc(call: types.CallbackQuery):
    _, r, c, s = call.data.split("_")
    msg = f"✅ **Верно!**\n{c} звучит как — **[{s}]**" if r == 'w' else f"❌ **Ошибка!**\n{c} это — **[{s}]**"
    await call.message.edit_text(msg, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Ещё?", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data.startswith("ans_"))
async def c_word(call: types.CallbackQuery):
    _, st, w, c, t, l = call.data.split("_")
    m = f"✅ **Верно!**\n**{w}** = **{c}**\nПроизношение: **[{t}]**" if st == 'w' else f"❌ **Ошибка!**\n**{w}** — это **{c}**\nПроизношение: **[{t}]**"
    await call.message.edit_text(m, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text=l), types.KeyboardButton(text="⬅️ В начало"))
    a
