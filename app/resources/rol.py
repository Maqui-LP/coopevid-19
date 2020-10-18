from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.rol import Rol
from app.helpers.auth import authenticated
from app.db_sqlalchemy import db_sqlalchemy
from app.helpers.granted import granted

db = db_sqlalchemy

#protected resources
def index():
    if not authenticated(session):
        abort(401)
    if not granted("rol_index"):
        abort(403)

    roles = Rol.query.all()
    return render_template("rol/index.html", roles=roles)

def new():
    if not authenticated(session):
        abort(401)
    if not granted("rol_new"):
        abort(403)

    return render_template("roles/new.html")

def create():
    
    data = request.form.to_dict()

    rol = Rol.query.filter(Rol.nombre == data.get("nombre")).first()
    if (rol is not None):
        flash("El rol ya existe")
        return redirect(url_for("roles_new"))

    new_rol = Rol(data)

    db.session.add(new_rol)
    db.session.commit()
    return redirect(url_for("rol_index"))


