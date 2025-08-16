import datetime

#Guardamos el Nombre del usuario 
def guardar_user(id,name,text,lat=None,lon=None):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log.txt", "a",encoding="UTF-8") as f:
        if lat is not None or lon is not None:
            f.writelines(f"[{fecha}] ({id}){name} : {text} LAT:{lat} LON:{lon}")
            f.write("\n")
        else:
            f.writelines(f"[{fecha}] ({id}){name} : {text}")
            f.write("\n")