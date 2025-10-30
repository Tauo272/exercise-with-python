import requests
from bs4 import BeautifulSoup
import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="Tulio",
    password="Flta,26109",
    database="lawyers"
)

cursor = dataBase.cursor()
sqlOrder = "insert into notClients (Name, IdMatricula, University, Direction, City, PostalCode, MobilePhone, NotMobilePhone, Gmail, HaveWeb) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

for i in range(1):

    url =  requests.get(f"https://colegioabogadostuc.org.ar/herramientas/padron/?pag={i}")
    urlParsed = BeautifulSoup(url.text, "html.parser")

    for j in urlParsed.find_all("div", "vent-popu"):

        data = j.text.replace("\n", "")
        data = data.replace("close", "")
        data = data.replace("Padrón de Abogados", "")
        data = data.replace("\xa0·\xa0", "")
        data = data.replace("E-mail: ", "|")
        data = data.replace("Móvil: ", "|")
        data = data.replace("Teléfonos/Fax: ", "|")
        data = data.replace("Dirección: ", "|")
        data = data.replace("Matrícula: ", "|")
        data = data.replace("Sitio Web: ", "|")
        data = data.replace("Localidad: ", "|")
        data = data.replace("Universidad: ", "|")
        data = data.replace(" |", "|")
        data = data.split("|")
        cursor.execute(sqlOrder, tuple(data))
        cursor.commit()
        
cursor.close()