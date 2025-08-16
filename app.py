from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
from dotenv import load_dotenv
from comandos import *  #Ya que son tantos importamos todos
from contenido import contenido
from respuesta_texto import responder_saludo, eco, comando_inexistente
#from apis_externas import ubicacion

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
#handler_location = MessageHandler(filters.LOCATION, ubicacion)


#HANDLER COMANDOS   #TODO LO QUE MANEJE COMANDOS VA A comandos.py | SI REQUIERE UNA API, LA API ESTARA EN apis_externas.py
app.add_handler(CommandHandler("start",start))  #Para /start
app.add_handler(CommandHandler("help",help))    #Para /help
app.add_handler(CommandHandler("info",info))    #Para /info
app.add_handler(CommandHandler("clima",clima))    #Para /clima
app.add_handler(CommandHandler("YT",youtube))   #Para /Youtube
app.add_handler(CommandHandler("criptos",criptos))   #Para /Criptos
app.add_handler(CommandHandler("dolar",dolar))   #Para /Dolar Hoy
app.add_handler(CallbackQueryHandler(botones_callback)) #Para Botones
app.add_handler(MessageHandler(filters.LOCATION, recibir_ubicacion))    #Recibe ubicaciones del usuario
app.add_handler(MessageHandler(filters.COMMAND, comando_inexistente))   #Para Comandos nulos

#HANDLER GENERAL
#app.add_handler(MessageHandler(filters.User(user_id= [ADMIN_ID]),admin))    #Only para admin
app.add_handler(handler_saludo)
app.add_handler(handler_texto)
app.add_handler(handler_media)

if __name__ == "__main__":
    print("Bot iniciado")
    app.run_polling()#Inicar el bot (modo polling)