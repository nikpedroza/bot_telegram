# archivo_async.py
import datetime
import asyncio
import aiomysql
import os
from dotenv import load_dotenv  #Credenciales del servidor

load_dotenv()

host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
port = 3307

#Conexion a la DB
async def conexionDB():
    #Conectar MySQL usando asincronia
    conn = await aiomysql.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        port=port        
        )
    print("=== CONEXION ESTABLECIDA ===")
    return conn

# Guardamos un usuario
async def guardar_user(conexion, cursor, id, name):
    try:
        insert = "INSERT INTO usuarios (telegram_id, username) VALUES (%s, %s)"
        parametros = (id, name)
        await cursor.execute(insert, parametros)
        await conexion.commit()
        print(f"Usuario {name} guardado correctamente")
    except Exception as e:
        await conexion.rollback()
        print(f"ERROR {e}")

# Guardamos los logs
async def guardar_log(id: int = None, name: str = None, text: str = None, lat=None, lon=None):
    if id is None:
        print("ERROR: telegram_id es None")
        return

    conexion = None
    cursor = None
    try:
        conexion = await conexionDB()
        async with conexion.cursor() as cursor:
            await cursor.execute("SET time_zone = '-03:00';")

            # Verificar si el usuario ya existe
            select = "SELECT 1 FROM usuarios WHERE telegram_id = %s"
            await cursor.execute(select, (id,))
            datos = await cursor.fetchone()

            if not datos:
                # Si no existe, insertamos el usuario
                await guardar_user(conexion, cursor, id, name)

            insert = "INSERT INTO log (telegram_id, comando) VALUES (%s, %s)"
            if lat is not None or lon is not None:
                text = f"{text} {lat} {lon}"

            parametros = (id, text)
            await cursor.execute(insert, parametros)
            await conexion.commit()
    except Exception as e:
        if conexion:
            await conexion.rollback()
        print(f"ERROR AL GUARDAR LOG: {repr(e)}")
    finally:
        if conexion:
            conexion.close()


# Crear tablas
async def crear_tablas():
    conexion = await conexionDB()
    try:
        async with conexion.cursor() as cursor:
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
            );"""
            await cursor.execute(tabla_usuarios)
            await cursor.execute(tabla_log)

            # Crear clave foránea si no existe
            db = os.getenv("DATABASE")
            await cursor.execute(f"""
                SELECT CONSTRAINT_NAME
                FROM information_schema.referential_constraints
                WHERE TABLE_NAME = 'log'
                AND CONSTRAINT_SCHEMA = '{db}'
                AND CONSTRAINT_NAME = 'fk_log_telegram_id'
            """)
            if not await cursor.fetchone():
                await cursor.execute("""
                    ALTER TABLE log
                    ADD CONSTRAINT fk_log_telegram_id
                    FOREIGN KEY (telegram_id) REFERENCES usuarios(telegram_id)
                """)
                print("Clave foránea creada")
            else:
                print("Clave foránea ya existe")

        return tabla_usuarios, tabla_log

    except Exception as e:
        await conexion.rollback()
        print(f"Error crear_tablas: {e}")
    finally:
        conexion.close()


# Main para ejecutar directamente
async def main():
    try:
        await crear_tablas()
        # Aquí podrías probar guardar_log u otras funciones
        # await guardar_log(123456, "usuario_test", "comando_test")
    except Exception as e:
        print("=== ERROR AL EJECUTAR ===")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
