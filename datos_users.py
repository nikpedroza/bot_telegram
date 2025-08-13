import datetime

#Guardamos el el Nombre del usuario 
def guardar_user(id,name,text):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("users.txt", "a", ) as f:
        f.writelines(f"[{fecha}] ({id}){name} : {text}")
        f.write("\n")