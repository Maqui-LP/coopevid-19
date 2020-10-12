from flask import redirect, render_template, request, url_for, session, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.helpers.auth import authenticated
from app.db_sqlalchemy import db_sqlalchemy

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

    new_user = User(data)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))