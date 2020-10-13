from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def login():
    return render_template("auth/login.html")


def authenticate():
    
    params = request.form
    password =  generate_password_hash(params['password'], method='sha256')
    user = User.query.filter(User.email == params["email"], User.password == password ).first()
    
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    session["user"] = user.email

    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
