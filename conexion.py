#ARCHIVO USADO EN CASO DE UTILIZACION DE MYSQL
import mysql.connector
from mysql.connector import Error
import os

host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
port = 3307

def conexionDB():
    conexion = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    if conexion.is_connected():
        print("=== CONEXION ESTABLECIDA ===")

    return conexion
