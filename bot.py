import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM = "أنت مهندس مدني وإنشائي خبير اسمك إنجنيو، متخصص في تصميم المنشآت الخرسانية والفولاذية، حسابات الأحمال والجسور، الكودات SBC وACI وAISC. تجيب باللغة العربية دائماً."

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🏗️ أهلاً! أنا إنجنيو مساعدك الهندسي الذكي. اسألني عن أي مسألة هندسية!")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    bot.send_chat_action(msg.chat.id, 'typing')
    try:
        prompt = SYSTEM + "\n\nسؤال المستخدم: " + msg.text
        response = model.generate_content(prompt)
        bot.reply_to(msg, response.text)
    except:
        bot.reply_to(msg, "⚠️ حدث خطأ، حاول مرة ثانية.")

bot.infinity_polling()

