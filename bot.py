import telebot
import requests
import os
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = "8750564605:AAFXPn1jhwXuacsCF6ra_1mc3NfUd3Whc6U"
API_URL = "https://loginvisionus.com/api/webhook/customer/create"
BEARER_TOKEN = "phsU7RcVMkIOZcjCVRuTn2OumLvOBhAMA8MIiR0AT11GNKxQnKPWnGrEenbxMyDN"
USER_ID = "BV4D3rLaqZ"
PACKAGE_ID = "7V01pzaDdO"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_data = {}

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🚀 *Visionus Ativo!*\nUse /teste para gerar seu acesso.", parse_mode="Markdown")

@bot.message_handler(commands=['teste'])
def start_trial(message):
    bot.send_message(message.chat.id, "Qual o seu *Nome*?", parse_mode="Markdown")
    user_data[message.chat.id] = {'step': 'nome'}

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    cid = message.chat.id
    if cid in user_data and user_data[cid]['step'] == 'nome':
        user_data[cid]['name'] = message.text
        user_data[cid]['step'] = 'email'
        bot.send_message(cid, "Agora o seu *E-mail*:", parse_mode="Markdown")
    elif cid in user_data and user_data[cid]['step'] == 'email':
        bot.send_message(cid, "⏳ *Gerando acesso no servidor...*")
        
        # CORREÇÃO AQUI: Ajuste nos nomes dos campos
        payload = {
            "userId": USER_ID,
            "packageId": PACKAGE_ID,
            "name": user_data[cid]['name'],
            "email": message.text
        }
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            # Aumentamos o tempo de espera (timeout) para 20 segundos
            response = requests.post(API_URL, json=payload, headers=headers, timeout=20)
            data = response.json()
            
            if response.status_code == 200 and ("username" in data or "data" in data):
                # Se os dados vierem dentro de um campo 'data'
                user_info = data.get("data", data)
                res = (
                    "✅ *TESTE GERADO!*\n\n"
                    f"👤 Usuário: `{user_info.get('username')}`\n"
                    f"🔑 Senha: `{user_info.get('password')}`\n"
                    "🌐 DNS: `http://cs.tvapp.shop:80`"
                )
                bot.send_message(cid, res, parse_mode="Markdown")
            else:
                bot.send_message(cid, "❌ O servidor recusou o pedido. Pode ser que este e-mail já tenha sido usado.")
        except Exception as e:
            bot.send_message(cid, "⚠️ O servidor IPTV demorou a responder. Tente novamente em 1 minuto.")
        
        del user_data[cid]

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
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
