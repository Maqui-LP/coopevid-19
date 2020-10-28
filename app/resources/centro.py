from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.granted import granted
from app.helpers.form_validation import validateUser, validateUpdateUser
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
from app.models.rol import Rol
from app.models.centro import Centro
from app.models.configuracion import Configuracion

db = db_sqlalchemy



def new():
    if not authenticated(session):
        abort(401)

    if not granted("usuario_new"):
        abort(403)

    return render_template("centro/new.html")

def index():
    if not authenticated(session):
        abort(401)

    centros = Centro.getAll()

    return render_template("centro/index.html", centros=centros)

def create():
    if not authenticated(session):
        abort(401)

    data = request.form.to_dict()
    data['status'] = False

    for each in data:
        print(each)

    nuevoCentro = Centro(data)

    db.session.add(nuevoCentro)
    db.session.commit()
    
    return redirect(url_for("centro_index"))
