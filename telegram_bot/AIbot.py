from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

import asyncio

import requests

 
road_fine_url = "http://127.0.0.1:8000/road_fine/"
tadbirkorlik_url = "http://127.0.0.1:8000/tadbirkorlik/"
bhm = 375000 
flag = ""

# Bot tokeningizni kiriting
BOT_TOKEN = "bot_token"


# Bot va dispatcher obyektlari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()




# Asosiy menyu
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Konstitutsiya moddalari")],
        [KeyboardButton(text="🚘 Yo'l harakati qoidalari")],
        [KeyboardButton(text="Tadbirkorlikka oid qonunlar")]
    ],
    resize_keyboard=True
)

# Ortga qaytish menyusi
back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Ortga qaytish")],
    ],
    resize_keyboard=True
)

# Start komandasi
@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    global flag
    flag = "start"
    await message.answer(
        "Assalomu alaykum! Botga xush kelibsiz! Quyidagi menyudan birini tanlang:", 
        reply_markup=menu_keyboard
    )



# Konstitutsiya moddalari
@router.message(F.text == "📚 Konstitutsiya moddalari")
async def send_info(message: types.Message):
    await message.answer(
        "Bu bo'limda siz Konstitutsiya moddalarini olishingiz mumkin.", 
        reply_markup=back_keyboard
    )

# Yo'l harakati qoidalari
@router.message(F.text == "🚘 Yo'l harakati qoidalari")
async def send_avto_menu(message: types.Message):
    avto_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yo'l belgilarini rasm orqali aniqlash")],
            [KeyboardButton(text="Yo'l harakatiga oid savol-javoblar")],
            [KeyboardButton(text="⬅️ Ortga qaytish")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Yo'l harakati qoidalari bo'limiga xush kelibsiz! Quyidagi menyudan birini tanlang:", 
        reply_markup=avto_menu
    )

# Yo'l belgilarini rasm orqali aniqlash
@router.message(F.text == "Yo'l belgilarini rasm orqali aniqlash")
async def image(message: types.Message):
    await message.answer("Iltimos, yo'l belgisi rasmini yuklang.", reply_markup=back_keyboard)

# Yo'l harakatiga oid savol-javoblar
@router.message(F.text == "Yo'l harakatiga oid savol-javoblar")
async def avto_qoida(message: types.Message):
    global flag
    flag = 'yol_jarima'
    await message.answer(
        "Yo'l harakatiga oid savollaringizga javob topishga yordam beraman.", 
        reply_markup=back_keyboard
    )

@router.message(F.text != "⬅️ Ortga qaytish")  # "Ortga qaytish" tugmasi bilan faqat ortga qaytish bo'lishi kerak
async def send_to_api(message: types.Message): 
    if flag == 'yol_jarima': 
        user_text = message.text  # Foydalanuvchi yuborgan matnni olish
        
        data = {
            "query": user_text,
        }

        response = requests.post(road_fine_url, json=data)
        if response.status_code == 200: 
            print(response.json())
            await message.answer(
                f"{response.json()['Qonunbuzarlik']}, Jarimadi {response.json()['Jarima (BHM)']} BHM = {response.json()['Jarima (BHM)']*bhm} so'm"
            )
            


# Tadbirkorlikka oid qonunlar
@router.message(F.text == "Tadbirkorlikka oid qonunlar")
async def send_business_laws(message: types.Message):
    global flag
    flag = 'tadbirkorlik'
    print(flag)
    await message.answer(
        "Bu bo'limda siz tadbirkorlikka oid qonunlarni o'rganishingiz mumkin.", 
        reply_markup=back_keyboard
    )


@router.message(F.text != "⬅️ Ortga qaytish")  # "Ortga qaytish" tugmasi bilan faqat ortga qaytish bo'lishi kerak
async def send_to_tadbirkorlik_api(message: types.Message): 
    if flag == 'tadbirkorlik': 
        user_text = message.text  # Foydalanuvchi yuborgan matnni olish
        
        data = {
            "query": user_text,
        }

        response = requests.post(tadbirkorlik_url, json=data)
        if response.status_code == 200: 
            print(response.json())
            await message.answer(
                f"Sarlavha: {response.json()['Sarlavha']}, Havola: {response.json()['Havola']}"
            )


# Ortga qaytish
@router.message(F.text == "⬅️ Ortga qaytish")
async def back_to_main_menu(message: types.Message):
    await message.answer("Asosiy menyuga qaytdingiz. Quyidagi menyudan birini tanlang:", reply_markup=menu_keyboard)

# Foydalanuvchi yuborgan matnni olish


# Botni ishga tushirish
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

