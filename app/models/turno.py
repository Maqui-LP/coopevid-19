from app.db_sqlalchemy import db_sqlalchemy
from datetime import date
from sqlalchemy.dialects.mysql import TIME

db = db_sqlalchemy

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer , primary_key = True)
    dia = db.Column(db.Date, unique=False, nullable=False)
    horaInicio = db.Column(TIME(), unique= False, nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    userId = db.Column(db.Integer, db.ForeingKey('users.id'))