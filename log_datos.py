import datetime
from mysql.connector import Error
from conexion import conexionDB
import os

def guardar_user(conexion,cursor,id,name):
    try:
        insert = "INSERT INTO usuarios (telegram_id,username) VALUES (%s,%s)"
        parametros = (id,name)
        cursor.execute(insert,parametros)
        conexion.commit()
        print(f"Usuario {name} guardado correctamente")
    except Exception as e:
        conexion.rollback()
        print(f"ERROR {e}")


#Guardamos los logs del usuario 
def guardar_log(id:int = None, username:str=None, text:str=None, lat=None, lon=None):
    print("DEBUG guardar_log")
    if id is None:
        print("ERROR: telegram_id es None")
        return
    print("DEBUG 2")
    conexion = None
    cursor = None
    print("DEBUG 3")
    try:
        print("DEBUG 4")
        conexion = conexionDB()
        print(f"DEBUG: conexion")
        cursor = conexion.cursor()
        cursor.execute("SET time_zone = '-03:00';")
        if id is None:
            print("ERROR: telegram_id es None")
            return

        # Verificar si el usuario ya existe
        select = "SELECT 1 FROM usuarios WHERE telegram_id = %s"
        cursor.execute(select, (id,))
        datos = cursor.fetchone()
         
        if not datos:
            # Si no existe, insertamos el usuario
            guardar_user(conexion, cursor, id, username)

        insert = "INSERT INTO log (telegram_id, comando) VALUES (%s, %s)"
        if lat is not None or lon is not None:
            text = f"{text} {lat} {lon}"

        parametros = (id, text)
        cursor.execute(insert, parametros)
        conexion.commit()
        print("Log guardado correctamente")

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"ERROR AL GUARDAR LOG: {repr(e)}")
    except Error as db_err:
        print(f"Error de base de datos: {db_err}")
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    

def crear_tablas():
    try:
        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios(
            id INT AUTO_INCREMENT PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            username VARCHAR(100),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
        tabla_log = """
        CREATE TABLE IF NOT EXISTS log(
            id INT AUTO_INCREMENT PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            comando TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        cursor.execute(tabla_usuarios)
        cursor.execute(tabla_log)

        try:
            db = os.getenv("DATABASE")
            # Verificar si la clave foránea existe
            cursor.execute("""
                SELECT CONSTRAINT_NAME
                FROM information_schema.referential_constraints
                WHERE TABLE_NAME = 'log'
                AND CONSTRAINT_SCHEMA = '{db}'
                AND CONSTRAINT_NAME = 'fk_log_telegram_id'
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    ALTER TABLE log
                    ADD CONSTRAINT fk_log_telegram_id
                    FOREIGN KEY (telegram_id) REFERENCES usuarios(telegram_id)
                """)
                print("Clave foránea creada")
            else:
                print("Clave foránea ya existe")
        except Error as e:
            print(f"Clave foránea ya existe Error: {e}")
    except Error as e:
        print(e)
        conexion.rollback()

    return tabla_usuarios,tabla_log


if __name__ == "__main__":
    try:
        conexion = conexionDB()
        cursor = conexion.cursor()

        crear_tablas()#Creamos tablas
        #consultas()

    except Error as e:
        print("=== ERROR AL CONECTAR CON LA BASE DE DATOS ===")
        print(e)

    finally:
        print("=== CONEXION CERRADA ===")
        cursor.close()
        conexion.close()
