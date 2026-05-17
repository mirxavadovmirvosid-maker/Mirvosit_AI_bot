import os
from threading import Thread
import telebot
from google import genai
from flask import Flask

# SIZNING TELEGRAM BOT TOKENINGIZ
BOT_TOKEN = "8917394328:AAHYp1VAZpMLltPbOEceE3-GsmX0OCh4uwY"

# SIZNING GEMINI API KALITINGIZ
GEMINI_KEY = "AIzaSyB62MjBDMf1SlqVoe52RIywT8Ktiq7h0"

bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_KEY)

app = Flask('')

@app.route('/')
def home():
    return "Bot yoniq!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men Mirvosit AI botiman. Menga istalgan savolingizni bering.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        user_text = message.text
        # Kengaytirilgan va tezkor yangi model versiyasi
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.reply_to(message, "Xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.")

if __name__=="__main__":
    # Serverni alohida oqimda yoqamiz
    t = Thread(target=run)
    t.start()
    
    print("🤖 Telegram AI Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()