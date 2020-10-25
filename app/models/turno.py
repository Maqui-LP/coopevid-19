from app.db_sqlalchemy import db_sqlalchemy
from datetime import date, datetime

db = db_sqlalchemy

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer , primary_key = True)
    dia = db.Column(db.Date, unique=False, nullable=False)
    horaInicio = db.Column(db.DateTime, nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    userId = db.Column(db.Integer, db.ForeingKey('users.id'))

    # No ponemos horaFin porque todos los turnos duran la misma cantidad de tiempo
    # Guardo userEmail y userId porque userEmail es con el mail que pidió 
    # el turno (puede cambiarse), el userId no cambia nunca