import os
import random
import re
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

TOKEN = os.environ.get('TOKEN')

# 📌 2. Frases literárias
frases = [
    "📚 'A leitura é para o intelecto o que o exercício é para o corpo.' – Joseph Addison",
    "📝 'Um livro é um sonho que você segura com as mãos.' – Neil Gaiman",
    "📖 'Ler é sonhar pela mão de outro.' – Fernando Pessoa"
]

# 📌 4. Clube do Livro
livros_da_semana = [
    "📘 *Livro da Semana*: '1984' – George Orwell",
    "📘 *Livro da Semana*: 'O Pequeno Príncipe' – Antoine de Saint-Exupéry",
    "📘 *Livro da Semana*: 'Capitães da Areia' – Jorge Amado"
]

# 📌 7. Quiz Literário
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

# 🎯 Verificação da resposta do quiz + filtro anti-spam
def resposta_quiz(update: Update, context: CallbackContext):
    texto_usuario = update.message.text.lower().strip()
    correta = context.user_data.get('resposta_correta')

    # 🔹 Bloqueia mensagens com links
    if re.search(r"http[s]?://|www\.", texto_usuario):
        return  # Ignora mensagens contendo links

    # 🔹 Só responde se for resposta válida do quiz
    if correta and texto_usuario in ['a', 'b', 'c']:
        if texto_usuario == correta:
            update.message.reply_text("✅ Acertou! Muito bem!")
        else:
            update.message.reply_text(f"❌ Errou! A resposta correta era: *{correta}*", parse_mode='Markdown')
        context.user_data['resposta_correta'] = None
    else:
        return  # Ignora qualquer outra mensagem

# 🎯 Função principal
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(
        "📚 Bem-vindo ao KindleMind! \n\nComandos disponíveis:\n/frase - Frase literária\n/clube - Livro da semana\n/livro [nome] - Buscar livro\n/quiz - Iniciar quiz"
    )))
    dp.add_handler(CommandHandler("frase", frase))
    dp.add_handler(CommandHandler("clube", clube))
    dp.add_handler(CommandHandler("livro", livro))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, resposta_quiz))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
