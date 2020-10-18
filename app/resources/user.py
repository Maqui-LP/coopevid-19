from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.granted import granted
from app.helpers.form_validation import validateUser, validateUpdateUser
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
from app.models.rol import Rol
from app.models.configuracion import Configuracion

db = db_sqlalchemy

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    if not granted("usuario_index"):
        abort(403)

    numero_pagina = request.args.get("numero_pagina")
    if numero_pagina:
        numero_pagina = int(numero_pagina) 
    print("*********************************************")
    print("El numero recibido es: ", numero_pagina)
    
    usuarios_totales = User.getAll()
    
    users = User.getAllPaginado(numero_pagina)

    print("Tamaño: ", len(users))

    cantidad_paginas = int((len(usuarios_totales) - 1) / Configuracion.getConfiguracion().paginacion)

    print("Cantiadad de paginas: ", cantidad_paginas)
    
    return render_template("user/index.html", users=users, cantidad_paginas=cantidad_paginas )


def new():
    if not authenticated(session):
        abort(401)

    if not granted("usuario_new"):
        abort(403)

    return render_template("user/new.html")

def roles():
    if not authenticated(session):
        abort(401)
    if not granted("usuario_update"):
        abort(403)

    user_id = request.args.get("user_id")
    user = User.getUserById(user_id)
    roles = Rol.getAll()
    return render_template("user/roles.html", user=user, roles=roles)

def modificarRoles():
    data = request.form.to_dict()
    
    user_id = request.args.get('user_id')
    
    User.setRoles(user_id, data)
    
    db.session.commit()
    return redirect(url_for("user_index"))


def create():
    data = request.form.to_dict()

    error = validateUser(data)
    if error:
        flash(error)
        return redirect(url_for("user_new"))

    hashed_pass = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_pass
    data['activo'] = True
    
    #user = User.query.filter(User.username == data.get("username")).first()
    user = User.getUserByUsername(data.get("username"))

    if(user is not None):
        flash("Ya existe un usuario con ese username")
        return redirect(url_for("user_new"))

    #user = User.query.filter(User.email == data.get("email")).first()
    user = User.getUserByEmail(data.get("email"))
    if(user is not None):
        flash("Ya existe un usuario con ese email")
        return redirect(url_for("user_new"))

    new_user = User(data)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))

def update():
    if not authenticated(session):
        abort(401)

    user_id = int(request.args.get("user_id"))
    data = request.form.to_dict()

    error = validateUpdateUser(data)
    if error:
        flash(error)
        return redirect(url_for("user_edit"))

    user2 = User.getUserByEmail(data.get("email"))

    if(user2 is not None and user2.id != user_id):
        flash("Ya existe un usuario con ese email")
        return redirect(url_for("user_index"))
    
    #user2 = User.query.filter(User.username == data.get("username"), User.id != user_id).first()
    user2 = User.getUserByUsername(data.get("username"))
    if(user2 is not None and user2.id != user_id):
        flash("Ya existe un usuario con ese username")
        return redirect(url_for("user_index"))

    data["updated_at"] = datetime.now()
    User.updateUser(user_id, data)

    
    db.session.commit()

    return redirect(url_for("user_index"))

def edit():
    if not authenticated(session):
        abort(401)
    if not granted("usuario_update"):
        abort(403)
    
    user_id = request.args.get("user_id")
    user = User.getUserById(user_id)

    return render_template("user/update.html", user=user)


def delete():
    if not granted("usuario_destroy"):
        abort(403)

    user_id = request.form.to_dict()
    user = User.getUserById(user_id["user_id"])
    if(user is None):
        flash("El usuario no existe")
        return redirect(url_for("user_index"))

    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for("user_index"))

def perfil():
    #otra forma seria-> data = dict(email=session.get("user"))
    #data = {"email": session.get("user")}

    user = User.getUserById(session.get("user"))

    return render_template("user/perfil.html", user=user)

def toogleUserActivity():
    if not granted("usuario_update"):
        abort(403)
    
    user_id = request.form.to_dict()
    User.toogleUsrActivity(user_id["user_id"])

    db.session.commit()

    return redirect(url_for("user_index"))

def searchUserPage():
    return render_template("/user/search.html")

def searchUsers():
    data = request.form.to_dict()
    nombre= "%{}%".format(data['nombre'])
    apellido = "%{}%".format(data['apellido'])
    estado = int(data['estado'])

    users = User.getByNameLastNameAndState(nombre, apellido, estado)

    return render_template("/user/search.html", users=users)

