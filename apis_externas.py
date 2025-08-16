#from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup #Importacion de interaccion con el usuario
#from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
#from log_users import guardar_user
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def download_YT():    #/YT downloader
    pass
    #RECIBIR LINKS DE YOUTUBE Y DEVOLVER VIDEOS

def obtener_clima(ciudad: str = None, lat: float = None, lon: float = None):
    CLIMA_API_KEY = os.getenv("API_CLIMA")
    if ciudad is not None:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={CLIMA_API_KEY}&units=metric&lang=es"
        r = requests.get(url)
    elif lat is not None and lon is not None:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={CLIMA_API_KEY}&lang=es&units=metric"
        r = requests.get(url)
    
    data = r.json()

    if r.status_code != 200:
        print(f"Error al obtener el clima: {data.get('message','desconocido')}")

    tiempo ={
        "clima" : data["weather"][0]["description"],
        "temp_actual" : data["main"]["temp"],
        "sensasion_termica" : data["main"]["feels_like"],
        "temp_min" : data["main"]["temp_min"],
        "temp_max" : data["main"]["temp_max"],
        "humedad" : data["main"]["humidity"]
    }
    return tiempo
