from app.db_sqlalchemy import db_sqlalchemy
from datetime import date
from sqlalchemy.dialects.mysql import TIME

db = db_sqlalchemy

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer , primary_key = True)
    dia = db.Column(db.Date, unique=False, nullable=False)
    horaInicio = db.Column(db.Time, unique= False, nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, data):
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print(f"{data['hora']}")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        self.dia = data['fecha']
        self.horaInicio = data['hora']
        self.userEmail = data['mail']
        self.userId = data['userId']
        print("***********************************************")
        print(f"{self.horaInicio}")
        print("***********************************************")
    
    @staticmethod
    def getAll():
        return Turno.query.all()