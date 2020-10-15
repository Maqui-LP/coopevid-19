from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime

db = db_sqlalchemy

# Protected resources
def index():
    users = User.query.all()
    return render_template("user/index.html", users=users)

def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


#def create():
 #   if not authenticated(session):
  #      abort(401)

   # conn = connection()
    #User.create(conn, request.form)    

def create():
    
    data = request.form.to_dict()
    hashed_pass = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_pass
    data['activo'] = True
    
    user = User.query.filter(User.username == data.get("username")).first()
    if(user is not None):
        flash("Ya existe un usuario con ese username")
        return
    user = User.query.filter(User.email == data.get("email").first())
    if(user is not None):
        flash("Ya existe un usuario con ese email")
        return

    new_user = User(data)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))

def update():
    if not authenticated(session):
        abort(401)

    user_id = request.args.get("user_id")
    data = request.form.to_dict()
    user2 = User.query.filter(User.email == data.get("email"), User.id != user_id).first()

    if (user2 is not None):
        flash("Ya existe un usuario con ese email")
        return
    
    user2 = User.query.filter(User.username == data.get("username"), User.id != user_id).first()
    if(user2 is not None):
        flash("Ya existe un usuario con ese username")
        return

    data["updated_at"] = datetime.now()
    user = User.query.filter(User.id == user_id).update(data)

    db.session.commit()
    
    return redirect(url_for("user_index"))

def edit():
    if not authenticated(session):
        abort(401)
    
    user_id = request.args.get("user_id")
    user = User.query.filter(User.id == user_id).first()

    return render_template("user/update.html", user=user)


def delete():
    user_id = request.args.get("user_id")
    user = User.query.filter(User.id == user_id).first()
    if(user is None):
        flash("El usuario no existe")
        return

    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for("user_index"))