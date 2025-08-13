from telegram import Update #Importacion de interaccion con el usuario
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datos_users import guardar_user   #Funcion que guarda lo que recibe de un usuario en un .txt
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")#Cargamos el Token
ADMIN_ID = int(os.getenv("ADMIN_ID"))#Id del admin por si necesita administrar desde Telegram

'''FUNCIONES UNICAMENTE PARA COMANDOS'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    #/start
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    nombre = update.effective_user.username
    await update.message.reply_text(f"Hola {nombre},soy un Nikito Bot\nEsto es un bot de prueba realizado por mi parte con fines educativos.\n\nTe gustaria ver que mas opciones tengo?")
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/help
    guardar_user(update.effective_user.username,update.message.text)
    await update.message.reply_text("Seccion Help")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/info
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("Seccion info")


'''FUNCIONES DESTINADAS A TEXTO'''
async def comando_inexistente(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Comando inexistente
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("Comando no reconocido. Usa /help para ver los disponibles")

async def responder_saludo(update: Update, context: ContextTypes.DEFAULT_TYPE): #Responde a un saludo tipico del User
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text("Hola como estas?")    
    
async def texto(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Only Texto
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text(update.message.text)  #Simplemente un Eco para que sea de prueba

    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola admin")




#Creamos la Applicacion
app = Application.builder().token(TOKEN).build()

#Filtros
filtro_saludo = filters.Regex(r"(?i)\b(hola|buenas)\b")
handler_saludo = MessageHandler(filtro_saludo, responder_saludo)
handler_texto = MessageHandler(filters.TEXT & ~filters.COMMAND, texto)


#HANDLER COMANDOS
app.add_handler(CommandHandler("start",start))  #Para /start
app.add_handler(CommandHandler("help",help))    #Para /help
app.add_handler(CommandHandler("info",info))    #Para /info
app.add_handler(MessageHandler(filters.COMMAND, comando_inexistente))   #Para Comandos nulos

#HANDLER TEXTO
#app.add_handler(MessageHandler(filters.User(user_id= [ADMIN_ID]),admin))    #Only para admin
app.add_handler(handler_saludo)
app.add_handler(handler_texto)

app.run_polling()#Inicar el bot (modo polling)