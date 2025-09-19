from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

# 🔑 Pon aquí tu token de BotFather
TOKEN = '8350003914:AAF8US3eE_moPR98Pvao-ig5ShllWyZKvKs'

# ✅ Lista de RSS ecuatorianos
RSS_FEEDS = [
    'https://www.elcomercio.com/rss/portada.xml',
    'https://www.eluniverso.com/rss/feed/noticias/',
    'https://www.primicias.ec/rss/',
    'https://www.expreso.ec/rss/noticias.xml',
    'https://www.ecuadortimes.net/rss/',
    'https://www.metroecuador.com.ec/rss/',
    'https://lahora.com.ec/rss',
    'https://www.eltelegrafo.com.ec/rss',
    'https://www.televicentro.com.ec/rss/noticias.xml',
    'https://www.primicias.ec/rss/politica-economia.xml'
]

# Función para obtener los titulares
def obtener_titulares():
    titulares = []
    for feed in RSS_FEEDS:
        try:
            respuesta = requests.get(feed, timeout=10)
            soup = BeautifulSoup(respuesta.content, 'xml')
            for item in soup.find_all('item')[:5]:  # Últimos 5 titulares por fuente
                titulo = item.title.text
                link = item.link.text
                titulares.append(f"{titulo}\n{link}")
        except Exception as e:
            titulares.append(f"Error al obtener RSS: {feed}")
    return "\n\n".join(titulares[:20])  # Muestra máximo 20 titulares

# Comando /titulares
def titulares(update: Update, context: CallbackContext):
    update.message.reply_text("Obteniendo titulares, espera un momento...")
    news = obtener_titulares()
    if news:
        update.message.reply_text(news)
    else:
        update.message.reply_text("No se pudieron obtener titulares en este momento.")

# Función principal
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("titulares", titulares))
    print("Bot iniciado...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
