import telebot
from google import genai
import os
from threading import Thread

# SIZNING TELEGRAM BOT TOKENINGIZ
BOT_TOKEN = "8917394328:AAHYp1VAZpMLltPbOEceE3-GsmX0OCh4uwY"

# SIZNING GEMINI API KALITINGIZ
GEMINI_KEY = "AIzaSyB62MjBDMf1SB1iQVoe52RIywT8KtiQ7h0"

bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_KEY)

# Server o'chib qolmasligi uchun soxta port ochamiz
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot yoniq!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

print("🤖 Telegram AI Bot muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men Universal AI botman. Menga xohlagan savolingizni bering, javob berishga harakat qilaman! 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi.")
        print(f"Xatolik: {e}")

if name == "main":
    # Serverni alohida oqimda yoqamiz
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()