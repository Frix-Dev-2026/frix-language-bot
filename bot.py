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
        "friend": ["друг", "[фрэнд]"], "money": ["деньги", "[мани]"], "home": ["дом", "[хоум]"],
        "apple": ["яблоко", "[эпл]"], "school": ["школа", "[скул]"], "book": ["книга", "[бук]"],
        "mother": ["мама", "[мазер]"], "father": ["папа", "[фазер]"], "sister": ["сестра", "[систер]"],
        "brother": ["брат", "[бразер]"], "sun": ["солнце", "[сан]"], "moon": ["луна", "[мун]"],
        "star": ["звезда", "[стар]"], "cat": ["кот", "[кэт]"], "dog": ["собака", "[дог]"],
        "car": ["машина", "[кар]"], "city": ["город", "[сити]"], "way": ["путь", "[уэй]"],
        "time": ["время", "[тайм]"], "day": ["день", "[дэй]"], "night": ["ночь", "[найт]"],
        "man": ["мужчина", "[мэн]"], "woman": ["женщина", "[вумэн]"], "child": ["ребенок", "[чайлд]"],
        "tree": ["дерево", "[три]"], "food": ["еда", "[фуд]"], "sky": ["небо", "[скай]"]
    },
    "Русский для Англичан 🇷🇺/🇬🇧": {
        "привет (privet)": ["hello", "[pree-vyet]"], "вода (voda)": ["water", "[va-da]"],
        "хлеб (khleb)": ["bread", "[hlyeb]"], "друг (drug)": ["friend", "[droog]"],
        "деньги (dengi)": ["money", "[dyen-gee]"], "дом (dom)": ["home", "[dom]"],
        "мама (mama)": ["mother", "[ma-ma]"], "книга (kniga)": ["book", "[k-nee-ga]"],
        "папа (papa)": ["father", "[pa-pa]"], "сестра (sestra)": ["sister", "[syes-tra]"],
        "брат (brat)": ["brother", "[brat]"], "солнце (solntse)": ["sun", "[soln-tse]"],
        "луна (luna)": ["moon", "[loo-na]"], "звезда (zvezda)": ["star", "[zvyez-da]"],
        "машина (mashina)": ["car", "[ma-shee-na]"], "город (gorod)": ["city", "[go-rat]"]
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
@dp.message(F.text == "⬅️ В начало / Main Menu")
async def cmd_start(message: types.Message):
    init_db()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Курс слов / Word Course 📚"))
    builder.add(types.KeyboardButton(text="Алфавит / Alphabet 🔡"))
    builder.adjust(1)
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\nВыбери раздел:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Алфавит / Alphabet 🔡")
async def select_alphabet(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="English Alphabet 🇬🇧"))
    builder.add(types.KeyboardButton(text="Русский алфавит 🇷🇺"))
    builder.add(types.KeyboardButton(text="⬅️ В начало / Main Menu"))
    builder.adjust(1)
    await message.answer("Какой алфавит показать?", reply_markup=builder.as_markup(resize_keyboard=True
