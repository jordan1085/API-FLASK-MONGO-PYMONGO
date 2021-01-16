from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo #modulo que ya integra flask y mongo
from werkzeug.security import generate_password_hash, check_password_hash #modulo para hashear pass
from bson import json_util #modulo para combertir de bson a json
from bson.objectid import ObjectId #comvertir el string de id a un object id

app = Flask(__name__)

#conexion a mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/apipython"
#pasamos la confi a pymongo
mongo = PyMongo(app) 


#Ruta para crear usuarios
@app.route('/usuarios', methods={'POST'})
def create_user():
    #Recibo los datos enviados de postman 
    username = request.json['username'] #<= postman
    password = request.json['password']
    email = request.json['email']

    if username and password and email: #validacion
        hashed_password = generate_password_hash(password) #hash

        # .db permite acceder a la base de datos (se creara la coleccion users sola)
        id = mongo.db.users.insert( #insertamos los datos / mongo devuelve id
            {'username': username, 'password': hashed_password, 'email': email}
        )
        
        #respuesta que vere en consola
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }

        return response
        
    else: 
        return not_found()

    return {'menssage': 'recived'}

#Ruta para listar usuarios
@app.route('/usuarios', methods={'GET'})
def get_users():
    users = mongo.db.users.find() #Mostrara los ussuarios en mongo
    response = json_util.dumps(users) #bson a json

    return Response(response, mimetype='application/json') #Response permite inprimir formateado el json

#Ruta para mostrar usuario por ID
@app.route('/usuarios/<id>', methods={'GET'})
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)

    return Response(response, mimetype='application/json')

#Error 404
@app.errorhandler(404)
def not_found(error=None):
    
    #jsonify permite pasar mas parametros a la respues como el tipo de status error
    response = jsonify({
        'message': 'Recurso no encontrado en la ruta: ' + request.url,
        'status': 404
    })
    response.status_code = 404

    return response


# Server
if __name__ == "__main__":
    app.run(debug=True)