from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def login():
    return render_template("auth/login.html")


def authenticate():
    
    params = request.form.to_dict()
    user = User.query.filter(User.email == params["email"]).first()
    
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    
    if not (check_password_hash(user.password, params.get('password'))):
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    if not user.activo == 1:
        flash("Tu usuario se encuentra desactivado comunicate para mas información")
        return redirect(url_for("auth_login"))

    session["user"] = user.id

    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
