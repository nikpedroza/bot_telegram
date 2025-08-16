from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
from dotenv import load_dotenv
from comandos import start, help, info, botones_callback
from contenido import contenido
from respuesta_texto import responder_saludo, eco, comando_inexistente

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")#Cargamos el Token
ADMIN_ID = int(os.getenv("ADMIN_ID"))#Id del admin por si necesita administrar desde Telegram

#Creamos la Applicacion
app = Application.builder().token(TOKEN).build()

#Filtros
filtro_saludo = filters.Regex(r"(?i)\b(hola|buenas)\b")
handler_saludo = MessageHandler(filtro_saludo, responder_saludo)
handler_texto = MessageHandler(filters.TEXT & ~filters.COMMAND, eco)
handler_media = MessageHandler(filters.AUDIO | filters.PHOTO | filters.VIDEO | filters.VOICE | filters.Sticker.ALL | filters.Document.ALL, contenido)


#HANDLER COMANDOS
app.add_handler(CommandHandler("start",start))  #Para /start
app.add_handler(CommandHandler("help",help))    #Para /help
app.add_handler(CommandHandler("info",info))    #Para /info
app.add_handler(MessageHandler(filters.COMMAND, comando_inexistente))   #Para Comandos nulos
app.add_handler(CallbackQueryHandler(botones_callback))

#HANDLER GENERAL
#app.add_handler(MessageHandler(filters.User(user_id= [ADMIN_ID]),admin))    #Only para admin
app.add_handler(handler_saludo)
app.add_handler(handler_texto)
app.add_handler(handler_media)

if __name__ == "__main__":
    print("Bot iniciado")
    app.run_polling()#Inicar el bot (modo polling)