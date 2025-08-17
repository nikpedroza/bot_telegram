from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from log_datos import guardar_log   #Funcion que guarda lo que recibe de un usuario en un .txt
import asyncio

async def comando_inexistente(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Comando inexistente
    user_id= update.effective_user.id
    username = update.effective_user.name
    messge_text = update.message.text if update.message else "Comando Inexistente"
    asyncio.create_task(guardar_log(id=user_id,name=username,text=messge_text))
    
    await update.message.reply_text("Comando no reconocido. Usa /help para ver los disponibles")

async def responder_saludo(update: Update, context: ContextTypes.DEFAULT_TYPE): #Responde a un saludo tipico del User
    user_id= update.effective_user.id
    username = update.effective_user.name
    messge_text = update.message.text if update.message else "ah saludado"
    asyncio.create_task(guardar_log(id=user_id,name=username,text=messge_text))

    await update.message.reply_text("Hola como estas?")    
    
async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Only eco
    user_id= update.effective_user.id
    username = update.effective_user.name
    messge_text = update.message.text if update.message else "ECO"
    asyncio.create_task(guardar_log(id=user_id,name=username,text=messge_text))

    await update.message.reply_text(update.message.text)  #Simplemente un Eco para que sea de prueba