from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.granted import granted
from app.helpers.form_validation import validateUser, validateUpdateUser
from app.helpers.xss_escape import escape_xss
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
from app.models.rol import Rol
from app.models.turno import Turno
from app.models.centro import Centro
from app.models.configuracion import Configuracion
from datetime import datetime

db = db_sqlalchemy



def new():
    if not authenticated(session):
        abort(401)

    if not granted("turno_create"):
        abort(403)

    centros= Centro.getAll()

    return render_template("turno/new.html", centros=centros)

def index():
    if not authenticated(session):
        abort(401)

    if not granted("turno_index"):
        abort(403)

    turnos = Turno.getDailyList()

    return render_template("turno/index.html", turnos=turnos)

def create():
    if not authenticated(session):
        abort(401)

    data = request.form.to_dict()
    data = escape_xss(data)

    user = User.getUserByEmail(data.get("mail"))
    if not user:
        flash("No existe un usuario con dicho email")
        return redirect(url_for("turno_new"))
    data['userId'] = User.getUserByEmail(data['mail']).id

    centro = Centro.getCentroById(data.get("centroId"))
    if not centro:
        flash("No existe dicho centro")
        return redirect(url_for("turno_new"))
    data['centroNombre'] = centro.name

    turno = Turno.getTurnoByHoraFechaCentro(data['hora'], data['fecha'], data['centroId'])
    if turno is not None:
        flash("El turno no está disponible")
        return redirect(url_for("turno_new"))

    nuevoTurno = Turno(data)

    db.session.add(nuevoTurno)
    db.session.commit()
    
    return redirect(url_for("turno_index"))

def delete():
    if not granted("turno_destroy"):
        abort(403)

    turno_id = request.form.to_dict()
    turno = Turno.getTurnoById(turno_id["turno_id"])
    if(turno is None):
        flash("El turno no existe")
        return redirect(url_for("turno_index"))

    db.session.delete(turno)
    db.session.commit()

    return redirect(url_for("turno_index"))

def update():
    if not authenticated(session):
        abort(401)

    turno_id = int(request.args.get("turno_id"))
    data = request.form.to_dict()
    data = escape_xss(data)
    
    #TODO: generar un validateTurnoUpdate

    turno_db = Turno.getTurnoById(turno_id)
    if(turno_db is None):
        flash("El turno no existe")
        #TODO: redireccionar a turno_update
        #TODO: en realidad evaluar este caso
        return redirect(url_for("turno_index"))
    
    turno_horario_fecha_db = Turno.getTurnoByHoraFechaCentro(data['horaInicio'], data['dia'], turno_db.centroId)
    if turno_horario_fecha_db is not None:
        flash("El horario no se encuentra disponible, seleccione otro horario")
        return render_template("turno/update.html", turno=turno_db)

    Turno.updateTurno(turno_id, data)

    db.session.commit()

    return redirect(url_for("turno_index"))

def edit():
    if not authenticated(session):
        abort(401)
    if not granted("turno_update"):
        abort(403)
    
    turno_id = request.args.get("turno_id")
    turno = Turno.getTurnoById(turno_id)

    return render_template("turno/update.html", turno=turno)

def searchTurnoPage():
    return render_template("/turno/search.html")

def searchTurnos():
    data = request.form.to_dict()
    data = escape_xss(data)

    centro= "%{}%".format(data['centro'])
    mail = "%{}%".format(data['mail'])

    turnos = Turno.getByCentroAndMail(centro, mail)

    return render_template("/turno/search.html", turnos=turnos)