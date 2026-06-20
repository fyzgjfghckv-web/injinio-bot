import os
import anthropic
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

SYSTEM = """أنت مهندس مدني وإنشائي خبير اسمك إنجنيو، متخصص في تصميم المنشآت الخرسانية والفولاذية، حسابات الأحمال والجسور، الكودات SBC وACI وAISC. تجيب باللغة العربية دائماً."""

user_histories = {}

@bot.message_handler(commands=['start'])
def start(msg):
    user_histories[msg.chat.id] = []
    bot.reply_to(msg, "🏗️ أهلاً! أنا إنجنيو مساعدك الهندسي الذكي. اسألني عن أي مسألة هندسية!")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    cid = msg.chat.id
    if cid not in user_histories:
        user_histories[cid] = []
    bot.send_chat_action(cid, 'typing')
    user_histories[cid].append({"role": "user", "content": msg.text})
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM,
            messages=user_histories[cid]
        )
        reply = resp.content[0].text
        user_histories[cid].append({"role": "assistant", "content": reply})
        bot.reply_to(msg, reply)
    except:
        bot.reply_to(msg, "⚠️ حدث خطأ، حاول مرة ثانية.")

bot.infinity_polling()
