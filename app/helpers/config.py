from flask import session
from app.models.configuracion import Configuracion

def getConfig():
    return Configuracion.getConfiguracion()
    