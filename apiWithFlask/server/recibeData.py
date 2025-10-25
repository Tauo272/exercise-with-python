from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="Tulio",
    password="*******",
    database="miabuela123"
)

cursor = db.cursor()

@app.route("/", methods=["POST"])
def reciveData():
    data = request.get_json()
    name = data.get("name")
    query = "insert into users (name) values (%s)"
    cursor.execute(query, (name,))
    db.commit()
    return jsonify({"data" : name}),200
app.run(debug=True)