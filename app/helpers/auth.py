from app.models.user import User
from flask import redirect, render_template, request, url_for, session, abort, jsonify, flash

def authenticated(session):
    print("******************************")
    print(session.get('user'))
    user = User.getUserById(session.get('user'))
    
    if user is not None and not user.activo == 1:
        flash("Tu usuario se encuentra desactivado comunicate para mas información")
        session.clear()
        return redirect(url_for("auth_login"))

    return session.get("user")
