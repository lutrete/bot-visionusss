import telebot
import requests
import os
import json
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÕES FIXAS ---
TOKEN_TELEGRAM = "8750564605:AAFXPn1jhwXuacsCF6ra_1mc3NfUd3Whc6U"
API_URL = "https://loginvisionus.com/api/webhook/customer/create"
BEARER_TOKEN = "phsU7RcVMkIOZcjCVRuTn2OumLvOBhAMA8MIiR0AT11GNKxQnKPWnGrEenbxMyDN"
USER_ID = "BV4D3rLaqZ"
PACKAGE_ID = "7V01pzaDdO"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_data = {}

# Servidor Web simples para o Render não desligar
app = Flask(__name__)
@app.route('/')
def home(): return "Servidor Visionus Ativo"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🚀 *Visionus Oficial*\n\nDigite /teste para gerar o seu acesso grátis agora.", parse_mode="Markdown")

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
        return

    if cid in user_data and user_data[cid]['step'] == 'email':
        email_cliente = message.text
        nome_cliente = user_data[cid]['name']
        bot.send_message(cid, "⏳ *A ligar ao servidor...*")
        
        # Dados exatamente como a API espera
        payload = {
            "userId": USER_ID,
            "packageId": PACKAGE_ID,
            "name": nome_cliente,
            "email": email_cliente
        }
        
        # Cabeçalhos "Blindados" (Fingindo ser um navegador)
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }

        try:
            # Faz a chamada com 30 segundos de espera
            response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            
            # Tenta ler a resposta
            try:
                data = response.json()
            except:
                data = {}

            if response.status_code == 200:
                # Verifica se os dados estão na raiz ou dentro de 'data'
                info = data.get("data", data) if isinstance(data, dict) else {}
                
                user = info.get("username")
                pw = info.get("password")
                
                if user and pw:
                    msg = (
                        "✅ *ACESSO LIBERADO!*\n\n"
                        f"👤 Usuário: `{user}`\n"
                        f"🔑 Senha: `{pw}`\n"
                        "🌐 DNS: `http://cs.tvapp.shop:80`"
                    )
                    bot.send_message(cid, msg, parse_mode="Markdown")
                else:
                    bot.send_message(cid, "❌ O servidor processou mas não devolveu login. Tente um e-mail diferente.")
            else:
                # Se der erro 400, 401, 500 etc
                bot.send_message(cid, f"❌ Erro no Servidor ({response.status_code}). Verifique se este e-mail já existe no sistema.")
        
        except Exception as e:
            bot.send_message(cid, "⚠️ O servidor demorou muito a responder. Tente novamente.")
        
        del user_data[cid]

if __name__ == "__main__":
    Thread(target=run_web).start()
    # skip_pending evita que o bot tente responder mensagens antigas de quando estava offline
    bot.infinity_polling(skip_pending=True)
