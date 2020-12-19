from app.db_sqlalchemy import db_sqlalchemy
from datetime import date, datetime, timedelta
from sqlalchemy.dialects.mysql import TIME
from app.models.configuracion import Configuracion

db = db_sqlalchemy

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer , primary_key = True)
    dia = db.Column(db.Date, unique=False, nullable=False)
    horaInicio = db.Column(db.Time, unique= False, nullable=False)
    userEmail = db.Column(db.String(255), nullable=False, unique=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    centroId = db.Column(db.Integer, db.ForeignKey('centros.id'))
    centroNombre = db.Column(db.String(255), nullable=False, unique=False)

    def __init__(self, data):
        self.dia = data['fecha']
        self.horaInicio = data['hora']
        self.userEmail = data['mail']
        self.userId = data['userId']
        self.centroId = data['centroId']
        self.centroNombre = data['centroNombre']
    
    @staticmethod
    def getAll():
        return Turno.query.all()

    @staticmethod
    def getTurnoByHoraFechaCentro(hora, fecha, centro):
        return Turno.query.filter(Turno.dia == fecha, Turno.horaInicio == hora, Turno.centroId == centro).first()
    
    @staticmethod
    def getDailyList():
        today = date.today()
        nextDay = today + timedelta(days=2)
        turnos = Turno.query.filter(Turno.dia >= today, Turno.dia <= nextDay).order_by(Turno.dia, Turno.horaInicio) 
        return turnos

    @staticmethod
    def getTurnoById(id):
        return Turno.query.filter(Turno.id == id).first()

    @staticmethod
    def updateTurno(id, data):
        data.pop('csrf_token')
        Turno.query.filter(Turno.id == id).update(data)

    @staticmethod
    def getByCentroAndMail(centro, mail):
        return Turno.query.filter(Turno.centroNombre.like(centro), Turno.userEmail.like(mail))

    @staticmethod
    def getDailyPaginado(numero_pagina):
        today = date.today()
        nextDay = today + timedelta(days=2)
        return Turno.query.filter(Turno.dia >= today, Turno.dia <= nextDay).order_by(Turno.dia, Turno.horaInicio).paginate(page=numero_pagina, per_page=Configuracion.getConfiguracion().paginacion).items

    @staticmethod
    def getSearchPaginado(numero_pagina, centro, mail):
        return Turno.query.filter(Turno.centroNombre.like(centro), Turno.userEmail.like(mail)).paginate(page=numero_pagina, per_page=Configuracion.getConfiguracion().paginacion).items

    @staticmethod
    def getByFechaCentro(centro, fecha):
        return Turno.query.filter(Turno.centroId == centro, Turno.dia == fecha).all()

    @staticmethod
    def get_quantity_for_centro_id(centro_id):
        return Turno.query.filter(Turno.centroId == centro_id).count()
        #si no llega a andar, probar con scalar() pasandole una func.count()
