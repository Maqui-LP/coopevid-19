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
from app.models.centro import Centro
from app.models.configuracion import Configuracion
from app.helpers.form_validation import validateCentro
from werkzeug.utils import secure_filename
import requests
import app
import random
import os

db = db_sqlalchemy


def new():
    if not authenticated(session):
        abort(401)

    if not granted("centro_create"):
        abort(403)

    municipios = getMunicipios()

    params = request.args.to_dict()
    params.pop('csrf_token', None)
    return render_template("centro/new.html", municipios=municipios, **params)

def index():

    if not authenticated(session):
        abort(401)

    if not granted("centro_index"):
        abort(403)

    numero_pagina = request.args.get("numero_pagina")
        
    if numero_pagina:
        numero_pagina = int(numero_pagina) 

    centros_totales = Centro.getAll()

    centros = Centro.getAllPaginado(numero_pagina)

    cantidad_paginas = int((len(centros_totales) - 1) / Configuracion.getConfiguracion().paginacion)

    return render_template("centro/index.html", centros=centros, cantidad_paginas=cantidad_paginas)

def create():
    if not authenticated(session):
        abort(401)
    
    data = request.form.to_dict()
    data = escape_xss(data)

    archive = request.files['visit_protocol']

    if not archive or archive.filename == '':
        flash("Archivo Invalido")
        exit(0)

    filename = secure_filename(archive.filename)
    filename = f"{filename}_{random.randint(1000,9999)}.pdf"
    
    error = validateCentro(data)
    if error:
        flash(error)
        return redirect(url_for("centro_new", **data))
    
    centro = Centro.getCentroByName(data.get('name'))
    if(centro is not None):
        flash("Ya existe un centro con ese nombre")
        return redirect(url_for("centro_new", **data))

    centro = Centro.getCentroByAddress(data.get('address'))
    if(centro is not None):
        flash("Ya existe un centro con esa direccion")
        return redirect(url_for("centro_new", **data))

    archive.save(os.path.join('app/static/uploads/' , filename))

    data['file_name'] = filename
    data['status'] = False    
    data['status_create'] = "ACEPTADO"

    nuevoCentro = Centro(data)

    db.session.add(nuevoCentro)
    db.session.commit()
    
    return redirect(url_for("centro_index"))

def delete():
    if not granted("centro_destroy"):
        abort(403)

    centro_id = request.form.to_dict()
    centro = Centro.getCentroById(centro_id["centro_id"])
    if(centro is None):
        flash("El centro no existe")
        return redirect(url_for("centro_index"))

    db.session.delete(centro)
    db.session.commit()

    return redirect(url_for("centro_index"))

def detalle():
    if not authenticated(session):
        abort(401)
    if not granted("centro_show"):
        abort(403)

    centro_id = request.args.get("centro_id")
    centro = Centro.getCentroById(centro_id)

    municipios = getMunicipios()

    municipio = None
    for each in municipios:
        if int(each) == centro.municipio_id:
            municipio = municipios[each] 

    return render_template("centro/detalle.html", centro=centro, municipio=municipio)

def edit():
    if not authenticated(session):
        abort(401)
    if not granted("centro_update"):
        abort(403)
    
    centro_id = request.args.get("centro_id")
    centro = Centro.getCentroById(centro_id)

    # utilizamos valores definidos por el usuario para cargar el formulario por defecto
    for key, val in request.args.items():
        if hasattr(centro, key):
            setattr(centro, key, val)

    municipios = getMunicipios()

    municipio = None
    for each in municipios:
        if int(each) == centro.municipio_id:
            municipio = municipios[each] 

    return render_template("centro/update.html", centro=centro, municipios=municipios, municipio=municipio)

def update():
    if not authenticated(session):
        abort(401)

    centro_id = int(request.args.get("centro_id"))
    data = request.form.to_dict()
    data = escape_xss(data)
    ############################################
    #archive = request.files['visit_protocol']

    #if not archive or archive.filename == '':
    #    flash("Archivo Invalido")
    #    exit(0)

    #filename = secure_filename(archive.filename)
    #filename = f"{filename}_{random.randint(1000,9999)}.pdf"

    #archive.save(os.path.join(MEDIA_PATH, filename))

    #data['file_name'] = filename
    #################################
    error = validateCentro(data)
    if error:
        flash(error)
        return redirect(url_for("centro_edit", centro_id=centro_id, **data))

    centro2 = Centro.getCentroByAddress(data.get("address"))

    if centro2 is not None and centro2.id != centro_id:
        flash("Ya existe un centro con esa direccion")
        return redirect(url_for("centro_edit", centro_id=centro_id, **data))

    centro2 = Centro.getCentroByName(data.get("name"))
    if centro2 is not None and centro2.id != centro_id:
        flash("Ya existe un centro con ese nombre")
        return redirect(url_for("centro_edit", centro_id=centro_id, **data))

    Centro.updateCentro(centro_id, data)
    
    db.session.commit()
    return redirect(url_for("centro_index"))

def getMunicipios():
    r = requests.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135')

    r = r.json()

    return r.get("data").get("Town")

def togglePublicacion():
    if not authenticated(session):
        abort(401)
    if not granted("centro_update"):
        abort(403)
    
    data = request.form.to_dict()
    centro_id = data["centro_id"]
    
    status_aprobacion = Centro.getStatusAprobacion(centro_id)
    if status_aprobacion != "ACEPTADO":
        flash("El centro debe estar aceptado")
        return redirect(url_for("centro_index"))

    Centro.togglePublicacion(centro_id)

    db.session.commit()

    return redirect(url_for("centro_index"))

def toggleAprobacion():
    if not authenticated(session):
        abort(401)
    if not granted("centro_update"):
        abort(403)
    
    data = request.form.to_dict()
    centro_id = data["centro_id"]
    Centro.toggleAprobacion(centro_id)

    db.session.commit()

    return redirect(url_for("centro_index"))


def definirStatusCreate():
    if not authenticated(session):
        abort(401)
    if not granted("centro_update"):
        abort(403)

    data = request.form.to_dict()
    data = escape_xss(data)

    Centro.definirStatusCreate(data["centro_id"], data["status_create"])

    db.session.commit()

    return redirect(url_for("centro_index"))

def searchCentrosPage():
    return render_template("/centro/search.html", statuses=Centro.getStatusesList())

def searchCentros():
    data = request.args.to_dict()
    data = escape_xss(data)
    name = "%{}%".format(data.get('name'))

    # Nos quedamos con los query params que empiezan con `status-` y le quitamos esa parte
    selected_statuses = [key.replace('status-', '') for key in data.keys() if key.startswith('status-')]
    
    numero_pagina = request.args.get("numero_pagina")
    if numero_pagina:
        numero_pagina = int(numero_pagina)    

    centros = Centro.getAllByNameStatusCreatePaginado(numero_pagina, name, selected_statuses)
    total = Centro.getAllByNameStatusCreate(name, selected_statuses).count()
    
    cantidad_paginas = int((total - 1) / Configuracion.getConfiguracion().paginacion)

    # Usamos este diccionario para recordar cuales son los estados seleccionados para el paginado
    status = {}
    for s in selected_statuses:
        status[f"status-{s}"] = "on"
    
    return render_template("/centro/search.html", statuses=Centro.getStatusesList(), status=status,
                           selected_statuses=selected_statuses, centros=centros,
                           cantidad_paginas=cantidad_paginas, name=data.get('name'))
    