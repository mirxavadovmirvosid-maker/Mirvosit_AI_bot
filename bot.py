import os
import telebot
from google import genai
from dotenv import load_dotenv

# .env faylini tizimga mutlaqo toza yuklaymiz
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Yangi obyektlarni yaratish
bot = telebot.TeleBot(BOT_TOKEN)
ai = genai.Client(api_key=GEMINI_KEY)

# /start buyrug'i kelganda
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Mirvosid AI botingiz 0 dan, eng yangi tizimda muvaffaqiyatli ishga tushdi! Menga istalgan savolingizni bering.")

# Har qanday matnli xabar kelganda
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        print(f"Kelgan xabar: {message.text}")
        
        # Google'ning eng yangi tekin modeli
        response = ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.reply_to(message, f"Xatolik yuz berdi. Tizim xabari: {e}")

if __name__=="__main__":
    print("🤖 Barcha tizimlar tozalandi. Yangi bot eshitishni boshladi...")
    bot.infinity_polling()