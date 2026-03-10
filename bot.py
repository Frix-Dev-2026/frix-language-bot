import asyncio, random, json, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ВНИМАНИЕ: Твой токен. Не передавай его посторонним!
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# --- БАЗА ДАННЫХ (JSON) ---
STATS_FILE = "users_stats.json"

def get_stats(user_id):
    if not os.path.exists(STATS_FILE):
        return {"xp": 0, "words_learned": 0}
    try:
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
        return data.get(str(user_id), {"xp": 0, "words_learned": 0})
    except: return {"xp": 0, "words_learned": 0}

def update_stats(user_id, xp_gain=10, word_plus=0):
    data = {}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
        except: data = {}
    
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"xp": 0, "words_learned": 0}
    
    data[uid]["xp"] += xp_gain
    data[uid]["words_learned"] += word_plus
    
    with open(STATS_FILE, "w") as f:
        json.dump(data, f)

# --- КОНТЕНТ (СЛОВАРЬ) ---
ABC = [("A", "эй"), ("B", "би"), ("C", "си"), ("D", "ди"), ("E", "и"), ("F", "эф")]

LESSONS = {
    "🍎 Фрукты": {"apple": ["яблоко", "эпл"], "banana": ["банан", "бэнэнэ"], "orange": ["апельсин", "орандж"]},
    "👨‍👩‍👧 Семья": {"mother": ["мама", "мазер"], "father": ["папа", "фазер"], "sister": ["сестра", "систер"]},
    "🚗 Транспорт": {"car": ["машина", "кар"], "bus": ["автобус", "бас"], "plane": ["самолет", "плейн"]},
    "🔢 Числа": {"one": ["один", "уан"], "two": ["два", "ту"], "three": ["три", "фри"]}
}

def main_kb():
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="Алфавит 🔡"), types.KeyboardButton(text="Профиль 👤"))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# --- ХЕНДЛЕРЫ ---
@dp.message(Command("start"))
@dp.message(F.text == "🏠 Главное меню")
async def start(m: types.Message):
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\nВыбери категорию для обучения:", reply_markup=main_kb())

@dp.message(F.text == "Профиль 👤")
async def show_profile(m: types.Message):
    s = get_stats(m.from_user.id)
    level = s['xp'] // 100
    await m.answer(f"👤 *Профиль: {m.from_user.first_name}*\n\n"
                   f"🎖 Уровень: {level}\n"
                   f"🧪 Опыт (XP): {s['xp']}\n"
                   f"📚 Выучено слов: {s['words_learned']}", parse_mode="Markdown")

@dp.message(F.text == "Алфавит 🔡")
async def q_abc(m: types.Message):
    char, sound = random.choice(ABC)
    kb = InlineKeyboardBuilder()
    # Берем 4 случайных звука для выбора
    options = [a[1] for a in ABC]
    random.shuffle(options)
    for s in options[:4]:
        res = 'w' if s == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=s, callback_data=f"abc_{res}_{char}_{sound}"))
    await m.answer(f"🔡 Урок Алфавита\nКак звучит буква: *{char}*?", reply_markup=kb.as_markup(row_width=2), parse_mode="Markdown")

@dp.message(F.text.in_(LESSONS.keys()))
async def start_w(m: types.Message):
    l = m.text
    word, d = random.choice(list(LESSONS[l].items()))
    corr, trans = d[0], d[1]
    
    # Варианты ответов из той же категории
    all_words = [v[0] for v in LESSONS[l].values()]
    random.shuffle(all_words)
    btns = all_words[:3]
    if corr not in btns: btns[0] = corr
    random.shuffle(btns)

    kb = InlineKeyboardBuilder()
    for b in btns:
        res = 'w' if b == corr else 'l'
        kb.add(types.InlineKeyboardButton(text=b
