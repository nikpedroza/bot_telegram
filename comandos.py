from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from log_users import guardar_user
import os

'''FUNCIONES UNICAMENTE PARA COMANDOS'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    #/start
    guardar_user(update.effective_user.id,update.effective_user.username,update.message.text)
    nombre = update.effective_user.username

    botones = [
        [InlineKeyboardButton("Ayuda",callback_data="btn_ayuda"),
         InlineKeyboardButton("Info",callback_data="btn_info")],
        [InlineKeyboardButton("Descargar Videos de Youtube",callback_data="btn_YT")],
        [InlineKeyboardButton("Salir",callback_data="btn_salir")]
    ]
    reply_markup = InlineKeyboardMarkup(botones)
    await update.message.reply_text(f"Hola <b>{nombre}</b>👋, soy Nikito Bot.\
                                    \nque te gustaria hacer?",parse_mode="HTML",reply_markup=reply_markup)
        
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/help
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_text = update.message.text if update.message else "Boton ayuda"
    guardar_user(user_id, username, message_text)

    respuesta = "/start : iniciar bot.\n/info : Datos sobre el bot\n/YT : Descargar videos de youtube\n/binance : obtener el precio de una criptomoneda\n/USD: " \
    "Obtener el precio del dolar a pesos"

    if  update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):     #/info
    user_id = update.effective_user.id
    username = update.effective_user.username    
    message_text = update.message.text if update.message else "Boton Info"
    guardar_user(user_id, username, message_text)  
    
    respuesta = ("Esto es un bot de prueba realizado por mi parte con fines educativos.\nEstoy realizando este bot en Python para expandir mis conocimiento mediante la practica" \
    " buscando la forma de realizar funciones nuevas y interesantes o entretenidas")

    if update.callback_query:
        await update.callback_query.message.reply_text(respuesta)
    else:
        await update.message.reply_text(respuesta)


async def botones_callback(update: Update,context: ContextTypes.DEFAULT_TYPE):
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
        await query.edit_message_text("De momento este sector esta en produccion")  #HACEEEEEEEEEEEEEEEEEEER
    elif query.data == "btn_salir":
        await query.delete_message()
        await context.bot.send_message(chat_id,"Adios, nos vemos la proxima")
    