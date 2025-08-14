from telegram import Update #Importacion de interaccion con el usuario
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from log_users import guardar_user   #Funcion que guarda lo que recibe de un usuario en un .txt
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")#Cargamos el Token
ADMIN_ID = int(os.getenv("ADMIN_ID"))#Id del admin por si necesita administrar desde Telegram


def descargas(nombre_archivo: str) -> str:  #Funcion de descarga
    download_dir = os.path.abspath("Descargas")
    os.makedirs(download_dir, exist_ok=True)
    return os.path.join(download_dir, os.path.basename(nombre_archivo))

def user_datos(user_id, username):
    guardar_user

'''FUNCIONES UNICAMENTE PARA COMANDOS'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    #/start
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    nombre = update.effective_user.username
    await update.message.reply_text(f"Hola <b>{nombre}</b>👋, soy Nikito Bot",parse_mode="HTML")
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/help
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("/start : iniciar bot.\n/info : Datos sobre el bot\n/YT : Descargar videos de youtube\n/binance : obtener el precio de una criptomoneda\n/USD: " \
    "Obtener el precio del dolar a pesos")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/info
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("Esto es un bot de prueba realizado por mi parte con fines educativos.\nRealizo este bot en Python para expandir mis conocimiento con practicas" \
    " buscando la forma de realizar funciones nuevas y interesantes o entretenidas")

async def download_YT():    #/YT downloader
    pass
    #RECIBIR LINKS DE YOUTUBE Y DEVOLVER VIDEOS


'''FUNCIONES DESTINADAS A TEXTO'''
async def comando_inexistente(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Comando inexistente
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    await update.message.reply_text("Comando no reconocido. Usa /help para ver los disponibles")

async def responder_saludo(update: Update, context: ContextTypes.DEFAULT_TYPE): #Responde a un saludo tipico del User
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text("Hola como estas?")    
    
async def texto(update: Update, context: ContextTypes.DEFAULT_TYPE):  #Only eco
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    print(update.effective_user.username,":",update.message.text)
    await update.message.reply_text(update.message.text)  #Simplemente un Eco para que sea de prueba


async def contenido(update: Update, context: ContextTypes.DEFAULT_TYPE): #Descargador de contenido

    #diccionario para mapear el tipo de mensaje a su atributo y texto de respuesta
    tipos = {
        "photo":{
            "file_id" : update.message.photo[-1].file_id if update.message.photo else None,
            "file_name" : None,
            "respuesta" : "Interesante foto"
        },
        "document":{
            "file_id": update.message.document.file_id if update.message.document else None,
            "file_name": update.message.document.file_name if update.message.document else None,
            "respuesta": "Buen contenido lo leere mas tarde, gracias :)"
        },
        "video": {
            "file_id": update.message.video.file_id if update.message.video else None,
            "file_name": update.message.video.file_name if update.message.video else None,
            "respuesta": "Buen video aunque soy ciego y no los puedo ver jeje"
        },
        "audio": {
            "file_id": update.message.audio.file_id if update.message.audio else None,
            "file_name": update.message.audio.file_name if update.message.audio else None,
            "respuesta": "Buen audio aunque no tengo oídos para escuchar jeje"
        }
    }
    if update.message.sticker:
        guardar_user(update.effective_user.id,update.effective_user.username, "Envio un Sticker")
        await update.message.reply_text("Buen sticker bro")
        return
    
    if update.message.voice:
        guardar_user(update.effective_user.id,update.effective_user.username, "Envio un mensaje de voz")
        await update.message.reply_text("No tengo oidos perdon :c")
        return

    for tipo,data in tipos.items(): #Buscar el tipo de archivo recibido
        if data["file_id"]:
            file_info = await context.bot.get_file(data["file_id"])
            #Si no hay nombre intenta usar el nombre de la url
            nombre_final = data["file_name"] or os.path.basename(file_info.file_path)

            ruta_final = descargas(nombre_final)    #Ruta
            await file_info.download_to_drive(ruta_final)   #Descarga

            guardar_user(update.effective_user.id, update.effective_user.username, f"{tipo.capitalize()} descargado en {ruta_final}")#Log
            return
    #Si no coincide con nada
    guardar_user(update.effective_user.id, update.effective_user.username, "Envio un tipo de contenido no soportado")
    await update.message.reply_text("Contenido no soportado. Porfavor, envia solo texto o comandos")
    
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola admin")




#Creamos la Applicacion
app = Application.builder().token(TOKEN).build()

#Filtros
filtro_saludo = filters.Regex(r"(?i)\b(hola|buenas)\b")
handler_saludo = MessageHandler(filtro_saludo, responder_saludo)
handler_texto = MessageHandler(filters.TEXT & ~filters.COMMAND, texto)
handler_media = MessageHandler(filters.AUDIO | filters.PHOTO | filters.VIDEO | filters.VOICE | filters.Sticker.ALL | filters.Document.ALL, contenido)


#HANDLER COMANDOS
app.add_handler(CommandHandler("start",start))  #Para /start
app.add_handler(CommandHandler("help",help))    #Para /help
app.add_handler(CommandHandler("info",info))    #Para /info
app.add_handler(MessageHandler(filters.COMMAND, comando_inexistente))   #Para Comandos nulos

#HANDLER GENERAL
#app.add_handler(MessageHandler(filters.User(user_id= [ADMIN_ID]),admin))    #Only para admin
app.add_handler(handler_saludo)
app.add_handler(handler_texto)
app.add_handler(handler_media)

app.run_polling()#Inicar el bot (modo polling)