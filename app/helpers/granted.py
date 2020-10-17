from flask import session
from app.models.user import User

def granted(permiso):
    print("*************************************************")
    print(session.get("user"))
    user = User.query.filter(User.id == session.get("user")).first()
    if(user is None):
        return False
    return permiso in User.getPermisos(user)

    