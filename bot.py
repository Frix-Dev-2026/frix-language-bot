import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ВНИМАНИЕ: ТВОЙ ТОКЕН УЖЕ ЗДЕСЬ!
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь уроков
LESSONS = {
    "English 🇬🇧": {
        "hello": ["привет", "[хелоу]"], "water": ["вода", "[уотер]"],
        "bread": ["хлеб", "[брэд]"], "apple": ["яблоко", "[эпл]"],
        "book": ["книга", "[бук]"], "school": ["школа", "[скул]"],
        "friend": ["друг", "[фрэнд]"], "money": ["деньги", "[мани]"]
    },
    "Russian 🇷🇺": {
        "privet": ["hello", "[pree-vyet]"], "voda": ["water", "[va-da]"],
        "hleb": ["bread", "[hlyeb]"], "kniga": ["book", "[k-nee-ga]"]
    }
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start_cmd(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡"))
    kb.adjust(1)
    await m.answer(f"Привет, {m.from_user.first_name}! 👋\nВыбери обучение:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def show_abc(m: types.Message):
    await m.answer("🔡 **English:** A [эй], B [би], C [си], D [ди]...\n🔡 **Русский:** А [A], Б [B], В [V], Г [G]...")

@dp.message(F.text == "Курс слов 📚")
@dp.message(F.text == "⬅️ Назад")
async def sel_lang(m: types.Message):
    kb = ReplyKeyboardBuilder()
    for l in LESSONS.keys():
        kb.add(types.KeyboardButton(text=l))
    kb.add(types.KeyboardButton(text="⬅️ В начало"))
    kb.adjust(1)
    await m.answer("Выбери язык:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(LESSONS.keys()))
async def start_quiz(m: types.Message):
    lang = m.text
    words = LESSONS[lang]
    word, data = random.choice(list(words.items()))
    correct, transcr = data[0], data[1]
    
    others = [v[0] for k, v in words.items() if k != word]
    options = random.sample(others, min(len(others), 2)) + [correct]
    random.shuffle(options)
    
    kb = InlineKeyboardBuilder()
    for opt in options:
        # Статус 'w' - успех, 'l' - проигрыш
        res = 'w' if opt == correct else 'l'
        # Обрезаем данные для кнопок, чтобы не было ошибок Telegram
        cb = f"ans_{res}_{word[:10]}_{correct[:10]}_{transcr[:10]}"
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=cb))
    kb.adjust(1)
    
    await m.answer(f"Курс: {lang}\nКак переводится: **{word}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("ans_"))
async def check_ans(call: types.CallbackQuery):
    d = call.data.split("_")
    status, word, correct, transcr = d[1], d[2], d[3], d[4]
    
    msg = f"✅ Правильно! \n{word} = {correct} {transcr}" if status == 'w' else f"❌ Ошибка. \n{word} = {correct} {transcr}"
    await call.message.edit_text(msg)
    
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Продолжим?", reply_markup=kb.as_markup(resize_keyboard=True))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
