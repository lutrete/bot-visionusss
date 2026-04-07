import telebot
import requests
import json

# ==========================================
# CONFIGURAÇÕES DO BOT (TOKEN FORNECIDO)
# ==========================================
TOKEN_TELEGRAM = "8750564605:AAFXPn1jhwXuacsCF6ra_1mc3NfUd3Whc6U"

# DADOS DA SUA API VISIONUS
API_URL = "https://loginvisionus.com/api/webhook/customer/create"
BEARER_TOKEN = "phsU7RcVMkIOZcjCVRuTn2OumLvOBhAMA8MIiR0AT11GNKxQnKPWnGrEenbxMyDN"
USER_ID = "BV4D3rLaqZ"
PACKAGE_ID = "7V01pzaDdO"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# Memória temporária para o fluxo de conversa
user_data = {}

# Mensagem de Boas-vindas
@bot.message_handler(commands=['start', 'ajuda'])
def send_welcome(message):
    welcome_text = (
        "🚀 *Bem-vindo ao Visionus Oficial!*\n\n"
        "O melhor sistema de entretenimento Sigma agora no seu Telegram.\n\n"
        "Comandos disponíveis:\n"
        "1️⃣ /teste - Gerar acesso grátis (2 horas)\n"
        "2️⃣ /planos - Ver preços de assinatura\n"
        "3️⃣ /suporte - Falar com um atendente"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# Exibir Planos
@bot.message_handler(commands=['planos'])
def send_plans(message):
    plans = (
        "💎 *TABELA DE PREÇOS VISIONUS*\n\n"
        "🥉 *MENSAL:* R$ 35,00\n"
        "🥈 *TRIMESTRAL:* R$ 85,00 (Recomendado)\n"
        "🥇 *SEMESTRAL:* R$ 150,00\n\n"
        "🔗 Para assinar, chame o suporte: /suporte"
    )
    bot.send_message(message.chat.id, plans, parse_mode="Markdown")

# Suporte
@bot.message_handler(commands=['suporte'])
def support(message):
    bot.send_message(message.chat.id, "👨‍💻 Nosso suporte humano atende aqui:\n👉 https://wa.me/5500000000000")

# INÍCIO DO FLUXO DE TESTE
@bot.message_handler(commands=['teste'])
def start_trial(message):
    bot.send_message(message.chat.id, "Para gerar seu teste, digite seu *Nome Completo*:", parse_mode="Markdown")
    user_data[message.chat.id] = {'step': 'nome'}

# CAPTURA DE RESPOSTAS (NOME E E-MAIL)
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    cid = message.chat.id
    
    # Passo 1: Receber o nome
    if cid in user_data and user_data[cid]['step'] == 'nome':
        user_data[cid]['name'] = message.text
        user_data[cid]['step'] = 'email'
        bot.send_message(cid, "Perfeito! Agora digite seu melhor *E-mail*:", parse_mode="Markdown")
        return

    # Passo 2: Receber o e-mail e Gerar na API
    if cid in user_data and user_data[cid]['step'] == 'email':
        email = message.text
        nome = user_data[cid]['name']
        
        bot.send_message(cid, "⏳ *Gerando seu acesso no servidor Sigma...*", parse_mode="Markdown")
        
        payload = {
            "userId": USER_ID,
            "packageId": PACKAGE_ID,
            "name": nome,
            "email": email
        }
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200 and "username" in data:
                result = (
                    "✅ *TESTE LIBERADO!*\n\n"
                    f"👤 *Usuário:* `{data['username']}`\n"
                    f"🔑 *Senha:* `{data['password']}`\n"
                    f"🌐 *DNS/URL:* `http://cs.tvapp.shop:80`\n\n"
                    "📺 *Dica:* Baixe o app *XCIPTV* ou *Smarters Pro* na sua loja de aplicativos."
                )
                bot.send_message(cid, result, parse_mode="Markdown")
            else:
                bot.send_message(cid, "❌ *Ops!* Você já gerou um teste nas últimas 24h ou o servidor está cheio. Tente novamente mais tarde.")
        
        except Exception as e:
            bot.send_message(cid, "⚠️ Erro ao conectar com o servidor. Tente novamente em instantes.")
        
        del user_data[cid] # Limpa a memória
        return

# Rodar o bot
print("🤖 Bot Visionus em execução...")
bot.infinity_polling()