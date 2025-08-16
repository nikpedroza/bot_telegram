from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from log_users import guardar_user   #Funcion que guarda lo que recibe de un usuario en un .txt


async def comando_inexistente(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Comando inexistente
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("Comando no reconocido. Usa /help para ver los disponibles")

async def responder_saludo(update: Update, context: ContextTypes.DEFAULT_TYPE): #Responde a un saludo tipico del User
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text("Hola como estas?")    
    
async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Only eco
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text(update.message.text)  #Simplemente un Eco para que sea de prueba