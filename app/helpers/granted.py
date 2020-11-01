from flask import session
from app.models.user import User
from app.models.configuracion import Configuracion

def granted(permiso):
    user = User.query.filter(User.id == session.get("user")).first()
    if user is None:
        return False
    
    permisos= User.getPermisos(user)

    if Configuracion.getStateOfSite() and "mantenimiento_admin" not in permisos:
        return False

    return permiso in permisos

    