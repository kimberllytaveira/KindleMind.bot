import os
import random
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

TOKEN = os.getenv("TOKEN") or "8365728614:AAHRusK1V34_ZHfeR4fUAbm0OVkje2Z4XMs"

# Frases literárias
frases = [
    "'A leitura é para o intelecto o que o exercício é para o corpo.' – Joseph Addison",
    "'Um livro é um sonho que você segura com as mãos.' – Neil Gaiman",
    "'Ler é sonhar pela mão de outro.' – Fernando Pessoa!"
]

# Clube do Livro
livros_da_semana = [
    "Livro da Semana: '1984' – George Orwell",
    "Livro da Semana: 'O Pequeno Príncipe' – Antoine de Saint-Exupéry",
    "Livro da Semana: 'Capitães da Areia' – Jorge Amado",
    "Livro da Semana: 'xÁgua Viva' – Clarice Lispector",
    "Livro da Semana: 'As mil partes do meu coração' – Collen Hoover",
    "Livro da Semana: 'Melhor do que nos filmes' – Lynn Painter"
	
]

# Quiz Literário
quiz_perguntas = [
    {
        "pergunta": "Quem escreveu Dom Casmurro?",
        "alternativas": ["a) Álvares de Azevedo", "b) Machado de Assis", "c) José de Alencar"],
        "correta": "b"
    },
    {
        "pergunta": "Qual autor criou o personagem Sherlock Holmes?",
        "alternativas": ["a) Agatha Christie", "b) Arthur Conan Doyle", "c) Edgar Allan Poe"],
        "correta": "b"
    },
    {
        "pergunta": "Em qual livro aparece o personagem Frodo Bolseiro?",
        "alternativas": ["a) O Hobbit", "b) O Senhor dos Anéis", "c) As Crônicas de Nárnia"],
        "correta": "b"
    },
    {
        "pergunta": "Quem é o autor da obra 'Cem Anos de Solidão'?",
        "alternativas": ["a) Gabriel García Márquez", "b) Pablo Neruda", "c) Jorge Luis Borges"],
        "correta": "a"
    },
    {
        "pergunta": "Qual destes livros foi escrito por Jane Austen?",
        "alternativas": ["a) Orgulho e Preconceito", "b) Grandes Esperanças", "c) Jane Eyre"],
        "correta": "a"
    },
    {
        "pergunta": "Quem escreveu a série 'O Príncipe Cruel'?",
        "alternativas": ["a) Holly Black", "b) Cassandra Clare", "c) Sarah J. Maas"],
        "correta": "a"
    },
    {
        "pergunta": "Qual livro conta a história de uma garota que enfrenta um coração partido e suas consequências?",
        "alternativas": [
            "a) Era Uma Vez Um Coração Partido - Bianca Sousa",
            "b) As Mil Partes do Meu Coração - Helena Gomes",
            "c) Melhor do Que Nos Filmes - Lauren Karcz"
        ],
        "correta": "a"
    },
    {
        "pergunta": "Em 'Melhor do Que Nos Filmes', qual é o tema central da história?",
        "alternativas": [
            "a) Um romance improvável entre estudantes universitários",
            "b) Uma jornada de fantasia em um reino encantado",
            "c) Um drama familiar intenso"
        ],
        "correta": "a"
    },
    {
        "pergunta": "Quem é o autor de 'As Mil Partes do Meu Coração'?",
        "alternativas": ["a) Collen Hoover", "b) Bianca Sousa", "c) Holly Black"],
        "correta": "a"
    },
    {
        "pergunta": "Qual destes livros é uma fantasia sombria com elementos de faerie?",
        "alternativas": [
            "a) O Príncipe Cruel - Holly Black",
            "b) Era Uma Vez Um Coração Partido - Bianca Sousa",
            "c) Melhor do Que Nos Filmes - Lauren Karcz"
        ],
        "correta": "a"
    }
]


# Função: /frase
def frase(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(frases))

# Função: /clube
def clube(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(livros_da_semana), parse_mode='Markdown')

# Função: /livro [termo de busca]
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

        resposta = f"{titulo}\n {autores}\n\n {descricao[:800]}..."
        update.message.reply_text(resposta, parse_mode='Markdown')
    except Exception as e:
        update.message.reply_text("Erro ao buscar o livro.")

# Função: /quiz
def quiz(update: Update, context: CallbackContext):
    q = random.choice(quiz_perguntas)
    texto = f"{q['pergunta']}\n\n" + "\n".join(q['alternativas']) + "\n\nResponda com 'a', 'b' ou 'c'"
    context.user_data['resposta_correta'] = q['correta']
    update.message.reply_text(texto)

# Verificação da resposta do quiz
def resposta_quiz(update: Update, context: CallbackContext):
    resposta = update.message.text.lower().strip()
    correta = context.user_data.get('resposta_correta')

    if correta and resposta in ['a', 'b', 'c']:
        if resposta == correta:
            update.message.reply_text("Acertou! Muito bem!")
        else:
            update.message.reply_text(f"Errou! A resposta correta era: {correta}", parse_mode='Markdown')
        context.user_data['resposta_correta'] = None

# Função principal
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Olá! Envie /frase, /clube, /livro ou /quiz")))
    dp.add_handler(CommandHandler("frase", frase))
    dp.add_handler(CommandHandler("clube", clube))
    dp.add_handler(CommandHandler("livro", livro))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, resposta_quiz))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
