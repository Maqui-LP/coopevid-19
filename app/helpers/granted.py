from flask import session
from app.models.user import User

def granted(permiso):

    user = User.query.filter(User.id == session.get("user")).first()

    return permiso in User.getPermisos(user)

    