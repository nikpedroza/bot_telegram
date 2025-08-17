from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from log_datos import guardar_log
import os
from apis_externas import obtener_clima

bandera_clima = False


'''FUNCIONES UNICAMENTE PARA COMANDOS'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    #/start
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton Start"
    guardar_log(id=user_id, username=username, text=message_text)
    nombre = update.effective_user.username

    botones = [
        [InlineKeyboardButton("Ayuda",callback_data="btn_ayuda"),
         InlineKeyboardButton("Info",callback_data="btn_info")],
        [InlineKeyboardButton("Descargar Videos de YT",callback_data="btn_YT"),
         InlineKeyboardButton("Clima",callback_data="btn_clima")],
        [InlineKeyboardButton("Salir",callback_data="btn_salir")]
    ]
    reply_markup = InlineKeyboardMarkup(botones)
    await update.message.reply_text(f"Hola <b>{nombre}</b>👋, soy Nikito Bot.\
                                    \nque te gustaria hacer?",parse_mode="HTML",reply_markup=reply_markup)
        
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/help
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton ayuda"
    guardar_log(id=user_id, username=username, text=message_text)

    respuesta = "/start : iniciar bot.\n/info : Datos sobre el bot\n/YT : Descargar videos de youtube\n/clima <ciudad>\n/criptos : obtener el precio de una criptomoneda\n/dolar: " \
    "Obtener el precio del dolar a pesos"

    if  update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/info
    user_id = update.effective_user.id
    username = update.effective_user.username    
    message_text = update.message.text if update.message else "Boton Info"
    guardar_log(user_id, username, message_text)  
    
    respuesta = ("Esto es un bot de prueba realizado por mi parte con fines educativos.\nEstoy realizando este bot en Python para expandir mis conocimiento mediante la practica" \
    " buscando la forma de realizar funciones nuevas y interesantes o entretenidas")

    if update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/YOUTUBE
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton Youtube"
    guardar_log(user_id, username, message_text)

    respuesta = "SECCION EN PREPARACION"

    if  update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):    #Clima
    global bandera_clima
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton Clima"
    guardar_log(user_id, username, message_text)
    
    if bandera_clima:
        #Esto en caso de que el usuario acceda desde un boton pidiendo el Clima
        teclado = [[KeyboardButton("Enviar  mi ubicacion",request_location=True)]]
        markup = ReplyKeyboardMarkup(teclado,resize_keyboard=True, one_time_keyboard=True)

        if  update.callback_query:  #Vino por /clima
            await update.callback_query.message.reply_text("Por favor compartí tu ubicación:", reply_markup=markup)
        else:#Vino por boton inline
            await update.message.reply_text("Por favor comparti tu ubicacion:", reply_markup=markup)

    else:
        #Caso comando con ciudad
        if not context.args:
            await update.message.reply_text("Usa: /clima <ciudad>")
            return
        
        ciudad = " ".join(context.args)
        info = obtener_clima(ciudad)
        respuesta = f"El clima en {ciudad} es {info["clima"].capitalize()}\nTemperatura actual: {info["temp_actual"]}°C\nTemp Min :{info["temp_min"]}°C \nTemp Max :{info["temp_max"]}\nHumedad:{info["humedad"]}°\n\nQue tenga un lindo dia"
        await update.message.reply_text(respuesta)

async def criptos(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/Criptos
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton Cripto"
    guardar_log(user_id, username, message_text)

    respuesta = "SECCION EN PREPARACION"

    if  update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def dolar(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/USD
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton USD"
    guardar_log(user_id, username, message_text)

    respuesta = "SECCION EN PREPARACION"

    if  update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):    #Recibir Ubicacion
    global bandera_clima
    user_location = update.message.location
    lat = user_location.latitude
    lon = user_location.longitude

    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Envio su Ubicacion"
    
    if bandera_clima:   #Verificamos que el usuario accedio desde un boton
        info = obtener_clima(lat=lat, lon=lon)
        respuesta = f"'{info["clima"].capitalize()}' en tu localidad \nTemperatura actual: {info["temp_actual"]}°C\nTemp Min :{info["temp_min"]}°C \nTemp Max :{info["temp_max"]}\nHumedad:{info["humedad"]}°\n\nQue tenga un lindo dia"
        await update.message.reply_text(respuesta)
        
        try:
            if lat or lon:
                guardar_log(user_id, username, message_text,lat,lon)
        except:
            guardar_log(user_id, username, message_text)
        bandera_clima = False   #Asi retorna a su estado anterior
    else:
        await update.message.reply_text("Linda ubicacion, espero que estes de vacaciones :)")
        guardar_log(user_id, username, "Envio una ubicacion",lat=lat,lon=lon)

async def botones_callback(update: Update,context: ContextTypes.DEFAULT_TYPE):
    global bandera_clima
    chat_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    if query.data == "btn_ayuda":
        await query.delete_message()
        await help(update,context)        
    elif query.data == "btn_info":
        await query.delete_message()
        await info(update,context)
    elif query.data == "btn_YT":
        await query.edit_message_text("DE MOMENTO LA SECCION ESTA EN PREPARACION")
        #await youtube(update,context)
    elif query.data == "btn_clima": 
        #Se activa una bandera porque en caso que el usuario pida el clima por un boton, te redirecciona a una seccion aparte
        await query.delete_message()
        bandera_clima = True
        await clima(update, context)
    elif query.data == "btn_salir":
        await query.delete_message()
        await context.bot.send_message(chat_id,"Adios, nos vemos la proxima")