from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

#conexion
app.config["MONGO_URI"] = "mongodb://localhost:27017/apipython"
mongo = PyMongo(app) #pasamos la confi

if __name__ == "__main__":
    app.run(debug=True)