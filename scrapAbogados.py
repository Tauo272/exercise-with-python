import mysql.connector
import requests
from bs4 import BeautifulSoup

dataBase = mysql.connector.connect(
    host="localhost",
    user="Tulio",
    password="Flta,26109",
    database="lawyers",
    charset="utf8mb4"
)

cursor = dataBase.cursor()

for page in range(352):

    try:

        url = requests.get(f"https://colegioabogadostuc.org.ar/herramientas/padron/?utm_source=chatgpt.com&pag={page}")
        beautyUrl = BeautifulSoup(url.text, "html.parser")
        urlParsed = beautyUrl.find_all("div", "vent-popu")

        for person in range(len(urlParsed)):

            personParsed = urlParsed[person].find("div", "vent").text
            personParsed = personParsed.replace("\n\nclose\nPadrón de Abogados", "").replace(" \xa0·\xa0 ", "\n").replace(" Sitio", "").strip().split("\n")
            jsonObject = {}
            for separate in personParsed:

                if separate in personParsed[0]:
                    jsonObject["name"]=separate

                elif separate in personParsed[-1]:
                    separate = separate.split(":")
                    passwordList = []
                    contentList = []

                    for i in separate:

                        i = i.replace(" ", "|").split("|")

                        if i[-1] in separate[-1]:
                            contentList.append(i[-1])
                            passwordList.append(i[0])
                            passwordList.pop(-1)
                        
                        else:
                            try:
                                passwordList.append(i[-1])
                                contentList.append(i[-2])
                            except:
                                continue

                    for passwordDictionary in range(len(passwordList)):
                        for contentDictionary in range(len(contentList)):
                            if passwordDictionary == contentDictionary:
                                jsonObject[passwordList[passwordDictionary]]=contentList[contentDictionary]

                else:
                    separate = separate.split(":")
                    jsonObject[f"{separate[0]}"]=separate[1]

            values = ", ".join(["%s"] * len(jsonObject))
            colums = ", ".join(f'`{i}`' for i in jsonObject.keys())
            sqlOrder = f"insert into notclients ({colums}) values ({values})"

            try:
                cursor.execute(sqlOrder, tuple(jsonObject[i] for i in jsonObject))
                dataBase.commit()
            except Exception as e:
                print(f"error: {e}")
                continue
        url.close()

    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        continue
    except requests.exceptions.Timeout as e:
        print(f"error: {e}")
        continue

cursor.close()
dataBase.close()