import telebot
import requests
import os
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

# --- WEB PLAYERS ---
WEB_BLINK = "http://webtv.iptvblinkplayer.com/"
WEB_SMARTERS = "http://webtv.iptvsmarters.com/"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_data = {}

# Servidor Flask para o Render não derrubar o bot
app = Flask(__name__)
@app.route('/')
def home():
    return "Visionus Bot está Online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- FUNÇÃO DO MENU ---
def menu_principal():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🚀 Gerar Teste Grátis'),
        types.KeyboardButton('💳 Planos e Valores'),
        types.KeyboardButton('📲 Baixar Aplicativos'),
        types.KeyboardButton('💻 Assistir no Navegador'),
        types.KeyboardButton('📖 Como Instalar?'),
        types.KeyboardButton('👨‍💻 Falar com Suporte')
    )
    return markup

# --- TRATAMENTO DE COMANDOS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    nome = message.from_user.first_name
    msg = (
        f"Olá {nome}! 👋\n\n"
        "Bem-vindo à *Visionus Premium*.\n"
        "Selecione uma opção abaixo no menu para continuar:"
    )
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=menu_principal())

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    cid = message.chat.id
    
    if message.text == '🚀 Gerar Teste Grátis':
        bot.send_message(cid, "Ótimo! Digite seu *NOME COMPLETO* para o registro:", parse_mode="Markdown")
        user_data[cid] = {'step': 'nome'}

    elif message.text == '💳 Planos e Valores':
        texto = (
            "💎 *TABELA DE PREÇOS*\n\n"
            "🥉 *MENSAL:* R$ 35,00\n"
            "🥈 *TRIMESTRAL:* R$ 85,00\n"
            "🥇 *SEMESTRAL:* R$ 150,00\n\n"
            "Chame o suporte para assinar!"
        )
        bot.send_message(cid, texto, parse_mode="Markdown")

    elif message.text == '📲 Baixar Aplicativos':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Vision XCIPTV", url=APK_XCIPTV))
        markup.add(types.InlineKeyboardButton("📥 Vision Smarters", url=APK_SMARTERS))
        markup.add(types.InlineKeyboardButton("📥 Vision Purple", url=APK_PURPLE))
        bot.send_message(cid, "👇 *Baixe o seu aplicativo abaixo:*", parse_mode="Markdown", reply_markup=markup)

    elif message.text == '💻 Assistir no Navegador':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Player 1", url=WEB_BLINK))
        markup.add(types.InlineKeyboardButton("🌐 Player 2", url=WEB_SMARTERS))
        bot.send_message(cid, "Acesse pelo seu Computador:", reply_markup=markup)

    elif message.text == '📖 Como Instalar?':
        msg = (
            "📖 *GUIA DE INSTALAÇÃO*\n\n"
            "1. Baixe o App na opção *Baixar Aplicativos*.\n"
            "2. Instale no seu aparelho.\n"
            "3. Use os dados gerados no seu teste.\n"
            "4. Servidor/DNS: `http://cs.tvapp.shop:80`"
        )
        bot.send_message(cid, msg, parse_mode="Markdown")

    elif message.text == '👨‍💻 Falar com Suporte':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Chamar no WhatsApp 🟢", url=LINK_WHATSAPP))
        bot.send_message(cid, "Clique no botão abaixo para suporte:", reply_markup=markup)

    # Lógica de Cadastro de Teste
    elif cid in user_data:
        if user_data[cid]['step'] == 'nome':
            user_data[cid]['name'] = message.text
            user_data[cid]['step'] = 'email'
            bot.send_message(cid, "Agora, digite seu *E-MAIL*:")
        
        elif user_data[cid]['step'] == 'email':
            email = message.text
            nome = user_data[cid]['name']
            bot.send_message(cid, "⏳ *A gerar o seu acesso...*")
            
            payload = {"userId": USER_ID, "packageId": PACKAGE_ID, "name": nome, "email": email}
            headers = {
                "Authorization": f"Bearer {BEARER_TOKEN}",
                "Content-Type": "application/json"
            }
            try:
                r = requests.post(API_URL, json=payload, headers=headers, timeout=25)
                d = r.json()
                info = d.get("data", d)
                res = (
                    "✅ *ACESSO LIBERADO!*\n\n"
                    f"👤 Usuário: `{info.get('username')}`\n"
                    f"🔑 Senha: `{info.get('password')}`\n"
                    "🌐 DNS: `http://cs.tvapp.shop:80`"
                )
                bot.send_message(cid, res, parse_mode="Markdown")
            except:
                bot.send_message(cid, "⚠️ Erro ao conectar com o painel.")
            del user_data[cid]

if __name__ == "__main__":
    # Inicia o servidor web
    Thread(target=run_web).start()
    # Inicia o bot
    bot.infinity_polling(skip_pending=True)
