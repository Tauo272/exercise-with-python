from flask import Flask, jsonify
import mysql.connector

class MyApi():

    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="Tulio",
            password="Flta,26109",
            database="miabuela123"
        )
        self.cursor = self.database.cursor()

    def startProgram(self):
        
        app = Flask(__name__)

        @app.route("/", methods=["GET"])
        def readAllDataBase():
            try:
                self.cursor.execute("select * from users")
                result = self.cursor.fetchall()
                print(result)
                
                return jsonify({"tables":result}),200
            
            except:
                return jsonify({"error":"404\n its cant find the database"})

        @app.route("/close", methods=["GET"])
        def close():
            self.cursor.close()
            self.database.close()
            return jsonify({"connection":"closed"}),200

        @app.route("/open", methods=["GET"])
        def open():
            self.database = mysql.connector.connect(
                host="localhost",
                user="Tulio",
                password="********",
                database="miabuela123"
            )
            self.cursor = self.database.cursor()
            return jsonify({"connection":"opened"}),200

        app.run(debug=True)

myClass = MyApi()
myClass.startProgram()