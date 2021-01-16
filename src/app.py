from flask import Flask, request, jsonify
from flask_pymongo import PyMongo #modulo que ya integra flask y mongo
from werkzeug.security import generate_password_hash, check_password_hash #modulo para hashear pass

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