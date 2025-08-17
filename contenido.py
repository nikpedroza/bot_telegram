import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from log_datos import guardar_log  #Funcion que hace un log en MySQL de lo que envia el usuario
import os


def descargas(nombre_archivo: str) -> str:  #Funcion de descarga
    download_dir = os.path.abspath("Descargas")
    os.makedirs(download_dir, exist_ok=True)
    return os.path.join(download_dir, os.path.basename(nombre_archivo))

async def contenido(update: Update, context: ContextTypes.DEFAULT_TYPE): #Descargador de contenido
    user_id= update.effective_user.id
    user_name = update.effective_user.name

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
        messge_text = update.message.text if update.message else "ECO"
        asyncio.create_task(guardar_log(id=user_id,name=user_name,text=messge_text))
        await update.message.reply_text("Buen sticker bro")
        return
    
    if update.message.voice:
        messge_text = update.message.text if update.message else "Envio un Audio"
        asyncio.create_task(guardar_log(id=user_id,name=user_name,text=messge_text))

        await update.message.reply_text("No tengo oidos perdon :c")
        return

    for tipo,data in tipos.items(): #Buscar el tipo de archivo recibido
        if data["file_id"]:
            messge_text = update.message.text if update.message else "Envio un Audio"
            asyncio.create_task(guardar_log(id=user_id,name=user_name,text=f"{tipo.capitalize()} descargado en {ruta_final}"))

            file_info = await context.bot.get_file(data["file_id"])
            #Si no hay nombre intenta usar el nombre de la url
            nombre_final = data["file_name"] or os.path.basename(file_info.file_path)

            ruta_final = descargas(nombre_final)    #Ruta
            await file_info.download_to_drive(ruta_final)   #Descarga

            return
    #Si no coincide con nada
    
    asyncio.create_task(guardar_log(id=user_id,name=user_name,text="envio un contenido no soportado"))
    await update.message.reply_text("Contenido no soportado. Porfavor, envia solo texto o comandos")
