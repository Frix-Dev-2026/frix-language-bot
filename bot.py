@dp.message(F.text == "Алфавит 🔡")
async def start_alpha_quiz(m: types.Message):
    char, sound = random.choice(ALPHABET_GAME)
    others = [s for c, s in ALPHABET_GAME if s != sound]
    options = random.sample(others, 2) + [sound]
    random.shuffle(options)
    
    kb = InlineKeyboardBuilder()
    for opt in options:
        res = 'w' if opt == sound else 'l'
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=f"abc_{res}_{char}_{sound}"))
    kb.adjust(1)
    await m.answer(f"Как звучит буква **{char}**?", reply_markup=kb.as_markup(), parse_mode="Markdown")
