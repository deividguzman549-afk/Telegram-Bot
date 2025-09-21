import os
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

# Obtener token del entorno
TOKEN = os.getenv("TOKEN")

# Fuente de noticias (Ejemplo: El Universo Ecuador)
URL = "https://www.eluniverso.com/rss/feed.xml"

def start(update, context):
    update.message.reply_text("👋 Hola, soy tu bot de titulares. Usa /noticias para ver lo más reciente.")

def noticias(update, context):
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")

        titulares = soup.find_all("item")[:5]  # primeros 5 titulares
        mensaje = "📰 *Últimos titulares:*\n\n"

        for item in titulares:
            titulo = item.title.text
            link = item.link.text
            mensaje += f"• [{titulo}]({link})\n"

        update.message.reply_text(mensaje, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        update.message.reply_text("⚠️ Error al obtener titulares.")
        print(f"Error en noticias: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("noticias", noticias))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
