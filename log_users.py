import datetime

#Guardamos el Nombre del usuario 
def guardar_user(id,name,text):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log.txt", "a", ) as f:
        f.writelines(f"[{fecha}] ({id}){name} : {text}")
        f.write("\n")