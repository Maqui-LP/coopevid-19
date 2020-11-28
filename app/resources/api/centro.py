from flask import  jsonify, request, abort
from app.models.centro import Centro
from app.models.turno import Turno
from app.models.user import User
from app.helpers.form_validation import validateCentro
from werkzeug.utils import secure_filename
from app.db_sqlalchemy import db_sqlalchemy
from app.csrf import app_csrf
import random
import os
from datetime import date

csrf = app_csrf
db = db_sqlalchemy

MEDIA_PATH = 'app/static/uploads/'

@csrf.exempt
def index():
    page = int(request.args.get("page",1))
    
    centros_totales = Centro.getAll()
    centros = Centro.getAllPaginado(page)
    json = []
    for centro in centros:
        dic = {
            "nombre": centro.name,
            "direccion": centro.address,
            "telefono": centro.phone,
            "hora_apertura":centro.openHour.isoformat(),
            "hora_cierre":centro.closeHour.isoformat(),
            "web":centro.web,
            "email":centro.mail
        }
        json.append(dic)
    return jsonify(centros=json, total=len(centros_totales), page=page)

@csrf.exempt
def getById(id):
    centro = Centro.getCentroById(id)

    if (centro is None):
        abort(404)

    json_centro =  {
        "nombre": centro.name,
        "direccion": centro.address,
        "telefono": centro.phone,
        "hora_apertura":centro.openHour.isoformat(),
        "hora_cierre":centro.closeHour.isoformat(),
        "web":centro.web,
        "email":centro.mail
    }

    return jsonify(centro = json_centro) 

@csrf.exempt
def create():
    data = request.form.to_dict()

    archive = request.files['visit_protocol']

    if not archive or archive.filename == '':
        abort(400)

    filename = secure_filename(archive.filename)
    filename = f"{filename}_{random.randint(1000,9999)}.pdf"
    
    error = validateCentro(data)
    if error:
        abort(400)

    data['status'] = False    

    centro = Centro.getCentrobyName(data.get('name'))
    if(centro is not None):
        abort(400)

    centro = Centro.getCentroByAddress(data.get('address'))
    if(centro is not None):
        abort(400)

    archive.save(os.path.join(MEDIA_PATH, filename))

    data['file_name'] = filename
    data['status_create'] = "PENDIENTE"

    nuevoCentro = Centro(data)

    db.session.add(nuevoCentro)
    db.session.commit()
    
    #TODO obtener el objeto guardado y retornarlo como json

    json_centro =  {
        "id": nuevoCentro.id,
        "nombre": nuevoCentro.name,
        "direccion": nuevoCentro.address,
        "telefono": nuevoCentro.phone,
        "hora_apertura":nuevoCentro.openHour.isoformat(),
        "hora_cierre":nuevoCentro.closeHour.isoformat(),
        "web":nuevoCentro.web,
        "email":nuevoCentro.mail,
        "muncipio_id":nuevoCentro.municipio_id,
        "type_id":nuevoCentro.type_id,
        "lat":nuevoCentro.lat,
        "long":nuevoCentro.long
    }

    return jsonify(atributos = json_centro) 

@csrf.exempt
def reserva(id):

    data = request.json
    hora = data.get('hora')
    #fecha = data.get('dia')
    fecha = data.get('fecha')
    email = data.get('email_donante')

    data["fecha"] = fecha
    turnoDb = Turno.getTurnoByHoraFechaCentro(hora, fecha, id)

    if turnoDb is not None:
        abort(400)

    data["centroId"] = id
    centro = Centro.getCentroById(id)
    data["centroNombre"] = centro.name
    user = User.getUserByEmail(email)

    data["mail"] = user.email
    data["userId"] = user.id
    nuevoTurno = Turno(data)    

    db.session.add(nuevoTurno)
    db.session.commit()


    json_turno = {
        "centro_id": id,
        "email_donante": nuevoTurno.userEmail,
        "hora_inicio": nuevoTurno.horaInicio.strftime("%H:%M:%S"),
        "fecha": nuevoTurno.dia.strftime("%Y-%m-%d"),
    }

    return jsonify(atributos = json_turno) 

@csrf.exempt
def getTurnoByFecha(id):
    centro = Centro.getCentroById(id)
    if (centro is None):
        abort(404)
    
    data = request.args
    fecha = data.get('fecha', date.today())
    turnos_disponibles = ["09:00:00", "09:30:00", "10:00:00", "10:30:00", "11:00:00", "11:30:00", "12:00:00", "12:30:00", "13:00:00", "13:30:00", "14:00:00", "14:30:00", "15:00:00", "15:30:00"]
    turnos = Turno.getByFechaCentro(id, fecha)
    hora_turnos=[]
    for t in turnos:
        hora_turnos.append(t.horaInicio.strftime("%H:%M:%S"))

    for i, td in enumerate(turnos_disponibles):
        if td in hora_turnos:
            turnos_disponibles.pop(i)

    json = []

    for turno in turnos_disponibles:
        dic = {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "horaInicio": turno,
            "centro":centro.name
        }
        json.append(dic)
    return jsonify(turnos=json)