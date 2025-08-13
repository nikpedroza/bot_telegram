from telegram import Update #Importacion de interaccion con el usuario
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from nombre_users import guardar_user   #Funcion que guarda lo que recibe de un usuario en un .txt
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")#Cargamos el Token

#Definicion de funciones asincronicas (Handlers)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):#Esta funcion se ejecuta cuando el usuario manda /start
    nombre = update.effective_user.username
    await update.message.reply_text(f"Hola {nombre},soy un bot")
    
    guardar_user(update.effective_user.username,update.message.text)

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):#Esta funcion repite lo que recibe
    await update.message.reply_text(update.message.text)
    print(update.effective_user.username,":",update.message.text)

    guardar_user(update.effective_user.username,update.message.text)
    

#Creamos la Applicacion (Nucleo del bot)
app = Application.builder().token(TOKEN).build()

#Añadir handlers (Que escucha el bot y como responde)
app.add_handler(CommandHandler("start",start))  #Para /start
app.add_handler(MessageHandler(filters.TEXT,eco))   #Para mensajes de texto

#Inicar el bot (modo polling)
app.run_polling()
