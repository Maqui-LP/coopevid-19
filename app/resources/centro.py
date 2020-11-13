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

MEDIA_PATH = './app/media/pdfs'

def new():
    if not authenticated(session):
        abort(401)

    if not granted("centro_create"):
        abort(403)

    municipios = getMunicipios()

    print("------------------------------------------------")
    for each in municipios:
        print(municipios[each])
    print("------------------------------------------------")

    return render_template("centro/new.html", municipios=municipios)

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

    return render_template("centro/index.html", centros=centros, cantidad_paginas=cantidad_paginas )

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
        return redirect(url_for("centro_new"))

    data['status'] = False    
    data['status_create'] = "ACEPTADO"
    
    centro = Centro.getCentrobyName(data.get('name'))
    if(centro is not None):
        flash("Ya existe un centro con ese nombre")
        return redirect(url_for("centro_new"))

    centro = Centro.getCentroByAddress(data.get('address'))
    if(centro is not None):
        flash("Ya existe un centro con esa direccion")
        return redirect(url_for("centro_new"))

    archive.save(os.path.join(MEDIA_PATH, filename))

    data['file_name'] = filename

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

    for each in municipios:
        print(type(each))
        print(type(centro.municipio_id))
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

    municipios = getMunicipios()

    for each in municipios:
        print(type(each))
        print(type(centro.municipio_id))
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
        return redirect(url_for("centro_index"))

    centro2 = Centro.getCentroByAddress(data.get("address"))

    if(centro2 is not None and centro2.id != centro_id):
        flash("Ya existe un centro con esa direccion")
        return redirect(url_for("centro_index"))

    centro2 = Centro.getCentrobyName(data.get("name"))
    if(centro2 is not None and centro2.id != centro_id):
        flash("Ya existe un centro con ese nombre")
        return redirect(url_for("centro_index"))

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
    Centro.togglePublicacion(centro_id)

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
    return render_template("/centro/search.html")

def searchCentros():
    data = request.args.to_dict()
    data = escape_xss(data)
    status = "%{}%".format(data.get('status'))
    name = "%{}%".format(data.get('name'))
    
    numero_pagina = request.args.get("numero_pagina")
    if numero_pagina:
        numero_pagina = int(numero_pagina)    

    centros = Centro.getAllByNameStatusCreatePaginado(numero_pagina, name, status)
    total = Centro.getAllByNameStatusCreate(name, status).count()
    
    cantidad_paginas = int((total - 1) / Configuracion.getConfiguracion().paginacion)
    
    return render_template("/centro/search.html", centros=centros, cantidad_paginas=cantidad_paginas, status=status, name=name)
    