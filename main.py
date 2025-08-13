import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Substitua pelo seu token
TOKEN = "8378976247:AAGwzpdTg4avT0RyBQnDjT0gFAcYEdRCO74" 

# Configuração de logs para depuração
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    await update.message.reply_text('Olá! Eu sou um bot literário. Use os comandos /citacao, /clube, /livro ou /quiz.')

# A partir daqui, você implementará as funcionalidades
async def citacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma citação literária aleatória."""
    # Código para buscar uma citação
    await update.message.reply_text("Aqui vai uma citação literária aleatória!")

async def clube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sugere um livro da semana."""
    await update.message.reply_text("O livro da semana é '1984', de George Orwell.")

async def livro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Busca resumo e dados do livro usando a API do Google Books."""
    # O usuário enviará "/livro [nome do livro]"
    livro_nome = " ".join(context.args)
    if not livro_nome:
        await update.message.reply_text("Por favor, digite o nome de um livro, ex: /livro O Pequeno Príncipe")
        return

    # Código para chamar a API do Google Books
    await update.message.reply_text(f"Buscando informações sobre o livro: {livro_nome}")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inicia um quiz literário."""
    await update.message.reply_text("Quiz: Quem escreveu 'Dom Casmurro'?")

def main() -> None:
    """Inicia o bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("citacao", citacao))
    application.add_handler(CommandHandler("clube", clube))
    application.add_handler(CommandHandler("livro", livro))
    application.add_handler(CommandHandler("quiz", quiz))

    application.run_polling()

if __name__ == '__main__':
    main()