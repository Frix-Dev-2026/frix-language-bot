import asyncio, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ВАШ ТОКЕН УЖЕ ЗДЕСЬ:
API_TOKEN = '8717727996:AAHyeVp3jshBS36Jhs7CzPfwRekyNntCi9Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь уроков
LESSONS = {
    "English 🇬🇧": {
        "hello": ["привет", "[хелоу]"], "water": ["вода", "[уотер]"],
        "bread": ["хлеб", "[брэд]"], "apple": ["яблоко", "[эпл]"],
        "book": ["книга", "[бук]"], "school": ["школа", "[скул]"]
    },
    "Russian 🇷🇺": {
        "privet": ["hello", "[pree-vyet]"], "voda": ["water", "[va-da]"]
    }
}

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ В начало")
async def start_cmd(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="Алфавит 🔡"))
    kb.adjust(1)
    await m.answer(f"Привет! Выбери обучение:", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит 🔡")
async def show_abc(m: types.Message):
    await m.answer("🔡 **English:** A, B, C, D, E...\n🔡 **Русский:** А, Б, В, Г, Д...")

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
async def start_lesson(m: types.Message):
    lang = m.text
    words_dict = LESSONS[lang]
    word, data = random.choice(list(words_dict.items()))
    translation, transcr = data[0], data[1]
    
    others = [v[0] for k, v in words_dict.items() if k != word]
    options = random.sample(others, min(len(others), 2)) + [translation]
    random.shuffle(options)
    
    kb = InlineKeyboardBuilder()
    for opt in options:
        # Упрощаем callback_data, чтобы не было ошибок
        cb = f"ans_{'w' if opt == translation else 'l'}_{word}_{translation}"
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=cb))
    kb.adjust(1)
    
    await m.answer(f"Курс: {lang}\nКак переводится: **{word}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("ans_"))
async def check_ans(call: types.CallbackQuery):
    d = call.data.split("_")
    status, word, correct = d[1], d[2], d[3]
    txt = f"✅ Правильно! \n{word} = {correct}" if status == 'w' else f"❌ Ошибка. \n{word} = {correct}"
    await call.message.edit_text(txt)
    
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="Курс слов 📚"), types.KeyboardButton(text="⬅️ В начало"))
    await call.message.answer("Играем дальше?", reply_markup=kb.as_markup(resize_keyboard=True))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
