from flask import  jsonify, request, abort
from app.models.centro import Centro
from app.helpers.form_validation import validateCentro
from werkzeug.utils import secure_filename
from app.db_sqlalchemy import db_sqlalchemy
from flask_wtf.csrf import CSRFProtect
import random
import os

csrf = CSRFProtect()

db = db_sqlalchemy

MEDIA_PATH = './app/media/pdfs'

@csrf.exempt
def index():
    page = int(request.args.get("page"))
    
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
        abort(404)

    filename = secure_filename(archive.filename)
    filename = f"{filename}_{random.randint(1000,9999)}.pdf"
    
    error = validateCentro(data)
    if error:
        abort(404)

    data['status'] = False    

    centro = Centro.getCentrobyName(data.get('name'))
    if(centro is not None):
        abort(404)

    centro = Centro.getCentroByAddress(data.get('address'))
    if(centro is not None):
        abort(404)

    archive.save(os.path.join(MEDIA_PATH, filename))

    data['file_name'] = filename

    nuevoCentro = Centro(data)

    db.session.add(nuevoCentro)
    db.session.commit()
    
    #TODO obtener el objeto guardado y retornarlo como json

    return "Whohw"
    