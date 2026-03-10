import asyncio, random, json, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiohttp import web # Добавили веб-сервер для Render

API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'
bot, dp = Bot(token=API_TOKEN), Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ ОБМАНА RENDER ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_webserver():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render передает порт в переменной окружения PORT
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# --- БАЗА ДАННЫХ (JSON) ---
STATS_FILE = "users_stats.json"

def get_stats(user_id):
    if not os.path.exists(STATS_FILE): return {"xp": 0, "words_learned": 0}
    try:
        with open(STATS_FILE, "r") as f: return json.load(f).get(str(user_id), {"xp": 0, "words_learned": 0})
    except: return {"xp": 0, "words_learned": 0}

def update_stats(user_id, xp_gain=10, word_plus=0):
    data = {}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f: data = json.load(f)
        except: data = {}
    uid = str(user_id)
    if uid not in data: data[uid] = {"xp": 0, "words_learned": 0}
    data[uid]["xp"] += xp_gain
    data[uid]["words_learned"] += word_plus
    with open(STATS_FILE, "w") as f: json.dump(data, f)

# --- КОНТЕНТ ---
LESSONS = {
    "🍎 Фрукты": {"apple": ["яблоко", "эпл"], "banana": ["банан", "бэнэнэ"]},
    "👨‍👩‍👧 Семья": {"mother": ["мама", "мазер"], "father": ["папа", "фазер"]},
    "🚗 Транспорт": {"car": ["машина", "кар"], "bus": ["автобус", "бас"]},
    "🔢 Числа": {"one": ["один", "уан"], "two": ["два", "ту"]}
}

def main_kb():
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys(): kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="Профиль 👤"))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
@dp.message(F.text == "🏠 Главное меню")
async def start(m: types.Message):
    await m.answer(f"Привет! 👋 Бот запущен на Render.\nВыбери урок:", reply_markup=main_kb())

@dp.message(F.text == "Профиль 👤")
async def show_profile(m: types.Message):
    s = get_stats(m.from_user.id)
    await m.answer(f"👤 *Профиль*\n🧪 Опыт: {s['xp']}\n📚 Слов: {s['words_learned']}", parse_mode="Markdown")

@dp.message(F.text.in_(LESSONS.keys()))
async def start_w(m: types.Message):
    l = m.text
    word, d = random.choice(list(LESSONS[l].items()))
    corr, trans = d[0], d[1]
    all_words = [v[0] for v in LESSONS[l].values()]
    random.shuffle(all_words)
    btns = all_words[:3]
    if corr not in btns: btns[0] = corr
    random.shuffle(btns)
    kb = InlineKeyboardBuilder()
    for b in btns:
