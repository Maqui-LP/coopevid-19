from flask import  jsonify, request, abort, flash
from app.models.centro import Centro
from app.models.turno import Turno
from app.models.user import User
from app.helpers.form_validation import validateCentro, validateReserve
from werkzeug.utils import secure_filename
from app.db_sqlalchemy import db_sqlalchemy
from app.csrf import app_csrf
import random
import os
from datetime import date
from app.models.configuracion import Configuracion

csrf = app_csrf
db = db_sqlalchemy

MEDIA_PATH = 'app/static/uploads/'

@csrf.exempt
def index():
    page = int(request.args.get("page",1))
    
    aux = 0 if (len(Centro.getAll()) % Configuracion.getConfiguracion().paginacion == 0)  else 1
    total_pages = int(len(Centro.getAll()) / Configuracion.getConfiguracion().paginacion) + aux
    centros = Centro.getAllPaginado(page)
    json = []
    for centro in centros:
        dic = {
            "id":centro.id,
            "nombre": centro.name,
            "direccion": centro.address,
            "telefono": centro.phone,
            "hora_apertura":centro.openHour.isoformat(),
            "hora_cierre":centro.closeHour.isoformat(),
            "web":centro.web,
            "email":centro.mail
        }
        json.append(dic)
    return jsonify(centros=json, total_pages=total_pages, page=page)

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
    data = request.json

    data['status'] = False    

    centro = Centro.getCentroByName(data.get('name'))
    if(centro is not None):
        abort(400, "Ya existe un centro con ese nombre")

    centro = Centro.getCentroByAddress(data.get('address'))
    if(centro is not None):
        abort(400, "Ya existe un centro con esa direccion")

    data['status_create'] = "PENDIENTE"
    data['file_name'] = " "

    data["type_id"]=str(data["type_id"])
    data["lat"]=str(data["lat"])
    data["long"]=str(data["long"])
    error = validateCentro(data)
    if error:    
        abort(400, "Informacion invalida")

    nuevoCentro = Centro(data)

    db.session.add(nuevoCentro)
    db.session.commit()
    
    json_centro =  {
        "id": nuevoCentro.id,
        "name": nuevoCentro.name,
        "address": nuevoCentro.address,
        "phone": nuevoCentro.phone,
        "openHour":nuevoCentro.openHour.isoformat(),
        "closeHour":nuevoCentro.closeHour.isoformat(),
        "web":nuevoCentro.web,
        "mail":nuevoCentro.mail,
        "muncipio_id":nuevoCentro.municipio_id,
        "type_id":nuevoCentro.type_id,
        "lat":nuevoCentro.lat,
        "long":nuevoCentro.long
    }

    return jsonify(centro = json_centro) 
    
@csrf.exempt
def reserva(id):

    data = request.json
    
    error = validateReserve(data)
    if error:
        abort(400, description="Peticion invalida, revise el formato de la misma")

    hora = data.get('hora')
    fecha = data.get('fecha')
    email = data.get('email')

    turnoDb = Turno.getTurnoByHoraFechaCentro(hora, fecha, id)

    if turnoDb is not None:
        abort(400)

    data["fecha"] = fecha
    data["centroId"] = id
    
    centro = Centro.getCentroById(id)
    data["centroNombre"] = centro.name
    
    user = User.getUserByEmail(email)
    if user is None:
        abort(400)

    data["mail"] = user.email
    data["userId"] = user.id

    nuevoTurno = Turno(data)    

    db.session.add(nuevoTurno)
    db.session.commit()


    json_turno = {
        "centro_id": id,
        "email_donante": nuevoTurno.userEmail,
        "hora": nuevoTurno.horaInicio.strftime("%H:%M:%S"),
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
            "hora": turno,
            "centro":centro.name
        }
        json.append(dic)
    return jsonify(turnos=json)

@csrf.exempt
def get_all_not_paginated():
    
    centros = Centro.get_all_published_centers()
    json = []
    for centro in centros:
        dic = {
            "id":centro.id,
            "nombre": centro.name,
            "direccion": centro.address,
            "telefono": centro.phone,
            "hora_apertura":centro.openHour.isoformat(),
            "hora_cierre":centro.closeHour.isoformat(),
            "web":centro.web,
            "email":centro.mail,
            "lat":centro.lat,
            "long":centro.long,
        }
        json.append(dic)
        
    return jsonify(centros=json)

@csrf.exempt
def get_estadisticas_tipo_centro():

    

    comida = Centro.get_all_comida()
    ropa = Centro.get_all_ropa()
    higiene_personal = Centro.get_all_higiene_personal()
    higiene_hogar = Centro.get_all_higiene_hogar()
    muebles = Centro.get_all_muebles()

    response = {
        "comida": comida,
        "ropa": ropa,
        "muebles": muebles,
        "higiene_personal":higiene_personal,
        "higiene_hogar": higiene_hogar
    }

    return jsonify(response = response)