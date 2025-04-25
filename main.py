import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# Bot tokenini BotFather’dan olingan token bilan almashtiring
TOKEN = "7701092354:AAEpm090WKlAcVfV_p42d29FMSl3R6igPpA"

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Qo‘shiqlar ma’lumotlari (yuqorida keltirilgan)
SONGS = {
    "Pop": [
        {"title": "Hello", "artist": "Adele", "link": "https://youtu.be/YQHsXMglC9A"},
        {"title": "Hey Jude", "artist": "The Beatles", "link": "https://youtu.be/A_MjCqQoLLA"},
        {"title": "Shape of You", "artist": "Ed Sheeran", "link": "https://youtu.be/JGwWNGJdvx8"}
    ],
    "Rock": [
        {"title": "Bohemian Rhapsody", "artist": "Queen", "link": "https://youtu.be/fJ9rUzIMcZQ"},
        {"title": "Paint It Black", "artist": "The Rolling Stones", "link": "https://youtu.be/O4irXQhgMqg"},
        {"title": "Come As You Are", "artist": "Nirvana", "link": "https://youtu.be/vabnZ9Exy9A"}
    ],
    "Folk / Country": [
        {"title": "Blowin’ in the Wind", "artist": "Bob Dylan", "link": "https://youtu.be/G58XWF6B3AA"},
        {"title": "Ring of Fire", "artist": "Johnny Cash", "link": "https://youtu.be/1WaV2x8molM"},
        {"title": "The Sound of Silence", "artist": "Simon & Garfunkel", "link": "https://youtu.be/4zLfCnGVeL4"}
    ],
    "Hip-Hop / Rap": [
        {"title": "Lose Yourself", "artist": "Eminem", "link": "https://youtu.be/_Yhyp-_hX2s"},
        {"title": "Hey Ya!", "artist": "OutKast", "link": "https://youtu.be/PWgvGjAhvIw"},
        {"title": "Gangsta’s Paradise", "artist": "Coolio", "link": "https://youtu.be/fPO76Jlnz6c"}
    ],
    "Jazz / Blues": [
        {"title": "What a Wonderful World", "artist": "Louis Armstrong", "link": "https://youtu.be/A3yCcXgbkrE"},
        {"title": "Summertime", "artist": "Ella Fitzgerald", "link": "https://youtu.be/u2bigf337aU"},
        {"title": "Blue Moon", "artist": "Billie Holiday", "link": "https://youtu.be/J2oEmPP5dTM"}
    ],
    "Bolalar qo‘shiqları": [
        {"title": "Twinkle Twinkle Little Star", "artist": "Traditional", "link": "https://youtu.be/yCjJyiqpAuU"},
        {"title": "Old MacDonald Had a Farm", "artist": "Traditional", "link": "https://youtu.be/_6HzoUcxRE0"},
        {"title": "The Wheels on the Bus", "artist": "Traditional", "link": "https://youtu.be/e_04ZrNroTo"}
    ]
}

# /start buyrug‘i
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Salom, <b>{message.from_user.full_name}</b>! Ingliz tilini o‘rganish uchun botga xush kelibsiz! "
        "Janr bo‘yicha qo‘shiqlar ro‘yxatini ko‘rish uchun /songs buyrug‘ini yozing."
    )

# /songs buyrug‘i: Janrlar ro‘yxatini ko‘rsatish
@dp.message(Command("songs"))
async def send_genres(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for genre in SONGS.keys():
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=genre, callback_data=genre)])
    await message.answer("Qo‘shiq janrini tanlang:", reply_markup=keyboard)

# Janr tanlanganda qo‘shiqlar ro‘yxatini yuborish
@dp.callback_query()
async def process_genre_selection(callback_query):
    genre = callback_query.data
    if genre in SONGS:
        songs = SONGS[genre]
        response = f"<b>{genre}</b> janridagi qo‘shiqlar:\n\n"
        for song in songs:
            response += f"🎵 <b>{song['title']}</b> – {song['artist']}\n"
            response += f"Listen: {song['link']}\n\n"
        await callback_query.message.answer(response)
    await callback_query.answer()

# Botni ishga tushirish
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
