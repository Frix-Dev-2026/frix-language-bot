import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ВАШ ТОКЕН
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# ДАННЫЕ УРОКОВ
ABC = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди"), ("E", "и"), ("F", "эф")]
LESSONS = {
    "English 🇬🇧": {"hello": ["привет", "хелоу"], "water": ["вода", "уотер"], "bread": ["хлеб", "брэд"]},
    "Russian 🇷🇺": {"privet": ["hello", "pree-vyet"], "kniga": ["book", "k-nee-ga"]}
}

def main_kb():
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="Алфавит 🔡"))
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
@dp.message(F.text == "🏠 Главное меню")
@dp.message(F.text == "⬅️ Назад")
async def start(m: types.Message):
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\nВыбери обучение:", reply_markup=main_kb())

@dp.message(F.text == "Алфавит 🔡")
async def q_abc(m: types.Message):
    char, sound = random.choice(ABC)
    kb = InlineKeyboardBuilder()
    for s in ["эй", "би", "си", "ди", "и", "эф"]:
        res = 'w' if s == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{res}_{char}_{sound}"))
    kb.adjust(2)
    nav = ReplyKeyboardBuilder().add(types.KeyboardButton(text="🏠 Главное меню")).as_markup(resize_keyboard=True)
    await m.answer(f"🔡 **Урок Алфавита**\nКак звучит буква: **{char}**?", reply_markup=kb.as_markup())

@dp.message(F.text.in_(LESSONS.keys()))
async def start_w(m: types.Message):
    l = m.text
    w, d = random.choice(list(LESSONS[l].items()))
    c, t = d[0], d[1]
    other_opts = [v[0] for v in LESSONS[l].values() if v[0] != c]
    opts = random.sample(other_opts, min(len(other_opts), 1)) + [c]
    random.shuffle(opts)
    
    kb = InlineKeyboardBuilder()
    for o in opts:
        # Обрезаем данные до 15 символов, чтобы влезть в лимит Telegram (64 байта)
        kb.add(types.InlineKeyboardButton(text=o, callback_data=f"ans_{'w' if o == c else 'l'}_{w[:15]}_{c[:15]}_{t[:15]}_{l[:15]}"))
    
    nav = ReplyKeyboardBuilder().add(types.KeyboardButton(text="⬅️ Назад"), types.KeyboardButton(text="🏠 Главное меню")).as_markup(resize_keyboard=True)
    await m.answer(f"🌍 **Курс: {l}**\nКак переводится: **{w}**?", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("abc_"))
async def c_abc(call: types.CallbackQuery):
    _, r, c, s = call.data.split("_")
    msg = f"✅ **Верно!**\nБуква **{c}** звучит как — **[{s}]**" if r == 'w' else f"❌ **Ошибка!**\nБуква **{c}** звучит как — **[{s}]**"
    await call.message.edit_text(msg, parse_mode="Markdown")
    kb = ReplyKeyboardBuilder().add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="🏠 Главное меню")).as_markup(resize_keyboard=True)
    await call.message.answer("Играем дальше? ✨", reply_markup=kb)

@dp.callback_query(F.data.startswith("ans_"))
async def c_word(call: types.CallbackQuery):
    d = call.data.split("_")
    st, word, corr, trans, lang = d[1], d[2], d[3], d[4], d[5]
    msg = f"✅ **Правильно!**\n**{word}** = **{corr}**\nПроизношение: **[{trans}]**" if st == 'w' else f"❌ **Ошибка!**\n
