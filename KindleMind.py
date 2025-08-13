import os
import random
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 📌 Pegando variáveis de ambiente
TOKEN = os.getenv("TOKEN")
APP_URL = os.getenv("APP_URL")  # ex: https://meu-bot.up.railway.app

# Flask app
app = Flask(__name__)

# Criar o updater e dispatcher
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# 📌 Frases literárias
frases = [
    "📚 'A leitura é para o intelecto o que o exercício é para o corpo.' – Joseph Addison",
    "📝 'Um livro é um sonho que você segura com as mãos.' – Neil Gaiman",
    "📖 'Ler é sonhar pela mão de outro.' – Fernando Pessoa"
]

# 📌 Clube do Livro
livros_da_semana = [
    "📘 *Livro da Semana*: '1984' – George Orwell",
    "📘 *Livro da Semana*: 'O Pequeno Príncipe' – Antoine de Saint-Exupéry",
    "📘 *Livro da Semana*: 'Capitães da Areia' – Jorge Amado"
]

# 📌 Quiz Literário
quiz_perguntas = [
    {
        "pergunta": "Quem escreveu *Dom Casmurro*?",
        "alternativas": ["a) Álvares de Azevedo", "b) Machado de Assis", "c) José de Alencar"],
        "correta": "b"
    }
]

# 🎯 Função: /frase
def frase(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(frases))

# 🎯 Função: /clube
def clube(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(livros_da_semana), parse_mode='Markdown')

# 🎯 Função: /livro [termo de busca]
def livro(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Digite o nome de um livro após o comando, ex: /livro dom casmurro")
        return

    termo = " ".join(context.args)
    url = f"https://www.googleapis.com/books/v1/volumes?q={termo}"

    try:
        res = requests.get(url)
        dados = res.json()
        if "items" not in dados:
            update.message.reply_text("Livro não encontrado 😕")
            return

        livro = dados["items"][0]["volumeInfo"]
        titulo = livro.get("title", "Sem título")
        autores = ", ".join(livro.get("authors", ["Desconhecido"]))
        descricao = livro.get("description", "Sem descrição.")

        resposta = f"📚 *{titulo}*\n👤 {autores}\n\n📝 {descricao[:800]}..."
        update.message.reply_text(resposta, parse_mode='Markdown')
    except Exception:
        update.message.reply_text("Erro ao buscar o livro.")

# 🎯 Função: /quiz
def quiz(update: Update, context: CallbackContext):
    q = random.choice(quiz_perguntas)
    texto = f"🎲 {q['pergunta']}\n\n" + "\n".join(q['alternativas']) + "\n\nResponda com 'a', 'b' ou 'c'"
    context.user_data['resposta_correta'] = q['correta']
    update.message.reply_text(texto)

# 🎯 Resposta do quiz
def resposta_quiz(update: Update, context: CallbackContext):
    resposta = update.message.text.lower().strip()
    correta = context.user_data.get('resposta_correta')

    if correta and resposta in ['a', 'b', 'c']:
        if resposta == correta:
            update.message.reply_text("✅ Acertou! Muito bem!")
        else:
            update.message.reply_text(f"❌ Errou! A resposta correta era: *{correta}*", parse_mode='Markdown')
        context.user_data['resposta_correta'] = None

# Handlers
dp.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Olá! Envie /frase, /clube, /livro ou /quiz")))
dp.add_handler(CommandHandler("frase", frase))
dp.add_handler(CommandHandler("clube", clube))
dp.add_handler(CommandHandler("livro", livro))
dp.add_handler(CommandHandler("quiz", quiz))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, resposta_quiz))

# Rota para receber mensagens do Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dp.process_update(update)
    return "ok"

# Rota para configurar o webhook
@app.route("/")
def set_webhook():
    updater.bot.setWebhook(f"{APP_URL}/{TOKEN}")
    return "Webhook configurado!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
