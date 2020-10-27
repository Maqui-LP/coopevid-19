from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.granted import granted
from app.helpers.form_validation import validateUser, validateUpdateUser
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
from app.models.rol import Rol
from app.models.configuracion import Configuracion

db = db_sqlalchemy

class centro:  
    def __init__(self, nombre, direccion, telefono):  
        self.nombre = nombre  
        self.direccion = direccion
        self.telefono = telefono

centros = []  

centros.append( centro('Iglesia Sagrado Corazón de Jesús', 'Diagonal 73 nro 1032', '221-5139019'))
centros.append( centro('Merendero Todos por una Sonrisa','Calle 88 nro 1912, Altos de San Lorenzo','221 - 5930941'))
centros.append( centro('La casita de Niquin', 'Calle 2 nro 3423', '221-754853'))
centros.append( centro('Pandemias eran las de antes','Calle 33 nro 787','221 - 7546534'))
centros.append( centro('Viva el Ejercito Popular Chino', 'Chinchin 123', '221-5139019'))
centros.append( centro('Dos mil gracias','Calle 88 nro 1912, Tolosa','221 - 56475385'))



def new():
    if not authenticated(session):
        abort(401)

    if not granted("usuario_new"):
        abort(403)

    return render_template("centro/new.html")

def index():
    if not authenticated(session):
        abort(401)

    return render_template("centro/index.html", centros=centros)

def create():
    if not authenticated(session):
        abort(401)

    data = request.form.to_dict()

    for each in data:
        print(each)

    return redirect(url_for("centro_index"))
