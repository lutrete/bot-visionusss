import telebot
import requests
import os
from flask import Flask
from threading import Thread

# ==========================================
# CONFIGURAÇÕES DO BOT E API
# ==========================================
TOKEN_TELEGRAM = "8750564605:AAFXPn1jhwXuacsCF6ra_1mc3NfUd3Whc6U"
API_URL = "https://loginvisionus.com/api/webhook/customer/create"
BEARER_TOKEN = "phsU7RcVMkIOZcjCVRuTn2OumLvOBhAMA8MIiR0AT11GNKxQnKPWnGrEenbxMyDN"
USER_ID = "BV4D3rLaqZ"
PACKAGE_ID = "7V01pzaDdO"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_data = {}

# --- SISTEMA PARA MANTER O RENDER ONLINE (FLASK) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Visionus está Online!"

def run():
    # O Render usa uma porta variável, por isso pegamos do sistema
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- COMANDOS DO TELEGRAM ---

@bot.message_handler(commands=['start', 'ajuda'])
def send_welcome(message):
    welcome_text = (
        "🚀 *Bem-vindo ao Visionus Oficial!*\n\n"
        "Comandos disponíveis:\n"
        "1️⃣ /teste - Gerar acesso grátis\n"
        "2️⃣ /planos - Ver preços\n"
        "3️⃣ /suporte - Falar com um atendente"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['planos'])
def send_plans(message):
    plans = (
        "💎 *TABELA VISIONUS*\n\n"
        "🥉 *MENSAL:* R$ 35,00\n"
        "🥈 *TRIMESTRAL:* R$ 85,00\n"
        "🥇 *SEMESTRAL:* R$ 150,00\n\n"
        "🔗 Suporte: /suporte"
    )
    bot.send_message(message.chat.id, plans, parse_mode="Markdown")

@bot.message_handler(commands=['suporte'])
def support(message):
    bot.send_message(message.chat.id, "👨‍💻 Suporte Humano:\n👉 https://wa.me/5500000000000")

@bot.message_handler(commands=['teste'])
def start_trial(message):
    bot.send_message(message.chat.id, "Para o teste, digite seu *Nome Completo*:", parse_mode="Markdown")
    user_data[message.chat.id] = {'step': 'nome'}

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    cid = message.chat.id
    if cid in user_data and user_data[cid]['step'] == 'nome':
        user_data[cid]['name'] = message.text
        user_data[cid]['step'] = 'email'
        bot.send_message(cid, "Agora, digite seu *E-mail*:", parse_mode="Markdown")
        return

    if cid in user_data and user_data[cid]['step'] == 'email':
        email = message.text
        nome = user_data[cid]['name']
        bot.send_message(cid, "⏳ *Gerando seu acesso...*", parse_mode="Markdown")
        
        payload = {"userId": USER_ID, "packageId": PACKAGE_ID, "name": nome, "email": email}
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json"}

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()
            if response.status_code == 200 and "username" in data:
                result = (
                    "✅ *TESTE LIBERADO!*\n\n"
                    f"👤 *Usuário:* `{data['username']}`\n"
                    f"🔑 *Senha:* `{data['password']}`\n"
                    f"🌐 *DNS/URL:* `http://cs.tvapp.shop:80`"
                )
                bot.send_message(cid, result, parse_mode="Markdown")
            else:
                bot.send_message(cid, "❌ Limite atingido ou erro no servidor.")
        except:
            bot.send_message(cid, "⚠️ Erro de conexão.")
        
        del user_data[cid]
        return

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    # Inicia o Flask em uma thread separada
    t = Thread(target=run)
    t.start()
    
    # Inicia o Bot do Telegram
    print("🤖 Bot Visionus em execução...")
    bot.infinity_polling()
