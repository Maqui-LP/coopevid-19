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
from app.helpers.form_validation import validateCentro
from werkzeug.utils import secure_filename
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

    return render_template("centro/new.html")

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

    centro = Centro.getCentroByPhone(data.get('phone'))
    if(centro is not None):
        flash("Ya existe un centro con ese telefono")
        return redirect(url_for("centro_new"))

    

    centro = Centro.getCentroByAddress(data.get('phone'))
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