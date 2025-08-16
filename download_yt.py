from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup #Importacion de interaccion con el usuario
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from log_users import guardar_user   #Funcion que guarda lo que recibe de un usuario en un .txt
import os
from dotenv import load_dotenv

async def download_YT():    #/YT downloader
    pass
    #RECIBIR LINKS DE YOUTUBE Y DEVOLVER VIDEOS