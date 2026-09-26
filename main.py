
import os
import telebot
from google import genai
from google.genai import types

# Récupération sécurisée des clés depuis l'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialisation du bot Telegram et du client Gemini
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bonjour ! Je suis ton assistant virtuel propulsé par Gemini. Comment puis-je t'aider aujourd'hui ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction="Tu es un assistant intelligent, utile et précis, parlant français."
            ),
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Oups, une erreur est survenue : {str(e)}")

print("Le bot est en cours d'exécution...")
bot.infinity_polling()
