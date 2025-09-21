import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8350003914:AAF8US3eE_moPR98Pvao-ig5ShllWyZKvKs"

# --- FUNCIONES DE COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aquí va la información que quieras enviar.")

# Ejemplo de función que hace scraping
async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://example.com/noticias"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Aquí suponemos que los titulares están en <h2>
    titulares = [h2.text for h2 in soup.find_all("h2")][:5]
    mensaje = "\n".join(titulares) if titulares else "No se encontraron noticias."
    
    await update.message.reply_text(mensaje)

# --- FUNCION PRINCIPAL ---
def main():
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Agregar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("noticias", get_news))
    
    # Iniciar el bot
    print("Bot iniciado...")
    app.run_polling()

# --- INICIO ---
if __name__ == "__main__":
    main()
