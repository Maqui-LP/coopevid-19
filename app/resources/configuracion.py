from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from app.helpers.auth import authenticated
from app.helpers.granted import granted
from app.db_sqlalchemy import db_sqlalchemy
from app.models.configuracion import Configuracion

def form():
    if not authenticated(session):
        abort(401)

    if not granted("configuracion_update"):
        abort(403)

    return render_template("/configuracion/update.html")

def update():
    data = request.form.to_dict()
    data["mantenimiento"] = int(data["mantenimiento"])
    Configuracion.updateConfiguracion(data)

    return render_template("/home.html")

