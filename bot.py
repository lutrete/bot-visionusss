import telebot
import requests
import os
import json
from flask import Flask
from threading import Thread
from telebot import types

# ==========================================
# CONFIGURAÇÕES DO BOT E API
# ==========================================
TOKEN_TELEGRAM = "8750564605:AAFXPn1jhwXuacsCF6ra_1mc3NfUd3Whc6U"
API_URL = "https://loginvisionus.com/api/webhook/customer/create"
BEARER_TOKEN = "phsU7RcVMkIOZcjCVRuTn2OumLvOBhAMA8MIiR0AT11GNKxQnKPWnGrEenbxMyDN"
USER_ID = "BV4D3rLaqZ"
PACKAGE_ID = "7V01pzaDdO"

# --- SUPORTE ---
LINK_WHATSAPP = "https://wa.me/5511954121162"

# --- LINKS DOS APPS ---
APK_XCIPTV = "https://tsrwuuwuvbwuhmlsfdlx.supabase.co/storage/v1/object/public/app-apks/1774947202036-4boo50neuxu.apk"
APK_SMARTERS = "https://tsrwuuwuvbwuhmlsfdlx.supabase.co/storage/v1/object/public/app-apks/1774947279679-d9d8hvrgi0q.apk"
APK_PURPLE = "https://tsrwuuwuvbwuhmlsfdlx.supabase.co/storage/v1/object/public/app-apks/1774960497482-wairbz6450f.apk"
WEB_BLINK = "http://webtv.iptvblinkplayer.com/"
WEB_SMARTERS = "http://webtv.iptvsmarters.com/"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_data = {}

app = Flask(__name__)
@app.route('/')
def home(): return "Visionus Ativo"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- FUNÇÃO DO MENU (REFORÇADA) ---
def menu_principal():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('🚀 Gerar Teste Grátis')
    btn2 = types.KeyboardButton('💳 Planos e Valores')
    btn3 = types.KeyboardButton('📲 Baixar Aplicativos')
    btn4 = types.KeyboardButton('💻 Assistir no Navegador')
    btn5 = types.KeyboardButton('📖 Como Instalar?')
    btn6 = types.KeyboardButton('👨‍💻 Falar com Suporte')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    nome = message.from_user.first_name
    texto = (
        f"Olá {nome}! 👋\n\n"
        "O seu menu foi atualizado! Se não estiver vendo os botões, tente enviar /start novamente."
    )
    # Enviamos a mensagem forçando o novo markup
    bot.send_message(message.chat.id, texto, parse_mode="Markdown", reply_markup=menu_principal())

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    cid = message.chat.id
    
    if message.text == '🚀 Gerar Teste Grátis':
        bot.send_message(cid, "Para começar, digite seu *NOME COMPLETO*:", parse_mode="Markdown")
        user_data[cid] = {'step': 'nome'}

    elif message.text == '💳 Planos e Valores':
        texto = (
            "💎 *PLANOS VISIONUS PREMIUM*\n\n"
            "🥉 *MENSAL:* R$ 35,00\n"
            "🥈 *TRIMESTRAL:* R$ 85,00\n"
            "🥇 *SEMESTRAL:* R$ 150,00\n\n"
            "Para assinar, chame o suporte!"
        )
        bot.send_message(cid, texto, parse_mode="Markdown")

    elif message.text == '📲 Baixar Aplicativos':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Vision XCIPTV", url=APK_XCIPTV))
        markup.add(types.InlineKeyboardButton("📥 Vision Smarters", url=APK_SMARTERS))
        markup.add(types.InlineKeyboardButton("📥 Vision Purple", url=APK_PURPLE))
        bot.send_message(cid, "Selecione o app para baixar:", reply_markup=markup)

    elif message.text == '💻 Assistir no Navegador':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Web Player 1", url=WEB_BLINK))
        markup.add(types.InlineKeyboardButton("🌐 Web Player 2", url=WEB_SMARTERS))
        bot.send_message(cid, "Acesse pelo seu computador:", reply_markup=markup)

    elif message.text == '📖 Como Instalar?':
        msg = "1. Baixe o App\n2. Instale\n3. DNS: `http://cs.tvapp.shop:80`"
        bot.send_message(cid, msg, parse_mode="Markdown")

    elif message.text == '👨‍💻 Falar com Suporte':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("WhatsApp Suporte 🟢", url=LINK_WHATSAPP))
        bot.send_message(cid, "Clique abaixo para falar conosco:", reply_markup=markup)

    # Fluxo de Teste
    elif cid in user_data:
        if user_data[cid]['step'] == 'nome':
            user_data[cid]['name'] = message.text
            user_data[cid]['step'] = 'email'
            bot.send_message(cid, "Agora, digite seu *E-MAIL*:")
        elif user_data[cid]['step'] == 'email':
            email = message.text
            nome = user_data[cid]['name']
            bot.send_message(cid, "⏳ Gerando acesso...")
            payload = {"userId": USER_ID, "packageId": PACKAGE_ID, "name": nome, "email": email}
            headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json"}
            try:
                r = requests.post(API_URL, json=payload, headers=headers, timeout=20)
                d = r.json()
                info = d.get("data", d)
                acesso = f"✅ *TESTE GERADO!*\n\n👤 Usuário: `{info.get('username')}`\n🔑 Senha: `{info.get('password')}`\n🌐 DNS: `http://cs.tvapp.shop:80`"
                bot.send_message(cid, acesso, parse_mode="Markdown")
            except:
                bot.send_message(cid, "⚠️ Falha. Tente novamente.")
            del user_data[cid]

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling(skip_pending=True)            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
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
