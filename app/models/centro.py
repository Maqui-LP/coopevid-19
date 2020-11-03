from app.db_sqlalchemy import db_sqlalchemy
from sqlalchemy.dialects.mysql import TIME
from app.models.turno import Turno
from app.models.configuracion import Configuracion

db = db_sqlalchemy

tipo_centro = db.Table('tipo_centro',
    db.Column('id', db.Integer, db.ForeignKey('centros.type_id'))
)

class Centro(db.Model):
    __tablename__ = 'centros'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone= db.Column(db.String(255), unique=False ,nullable=False)
    mail = db.Column(db.String(255), nullable = False)
    openHour= db.Column(TIME(), nullable=False)
    closeHour= db.Column(TIME(), nullable=False)
    type_id= db.Column(db.Integer, db.ForeignKey('tipo_centro.id'), nullable=False)
    web= db.Column(db.String , nullable=False)
    status = db.Column(db.Boolean,nullable=False)
    address = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    file_name = db.Column(db.String)
    turnos = db.relationship('Turno')

    #TODO: agregar el protocolo con formato PDF y el tema del municipio 
    #el municipio no se si tenemos que crear una clase municipio en base 
    #a la api de la catedra o solo poner el String con el nombre

    def __init__(self, data):
        self.name = data['name']
        self.phone = data['phone']
        self.mail = data['mail']
        self.openHour = data['openHour']
        self.closeHour = data['closeHour']
        self.type_id = data['type_id']
        self.web = data['web']
        self.status = data['status']
        self.address = data['address']
        self.lat = data['lat']
        self.long = data['long']
        self.file_name = data['file_name']
        
    @staticmethod
    def getAll():
        return Centro.query.all()
    
    @staticmethod
    def getCentroById(centro_id):
        return Centro.query.filter(Centro.id == centro_id).first()

    @staticmethod
    def getAllPaginado(numero_pagina):
        return Centro.query.paginate(page=numero_pagina, per_page=Configuracion.getConfiguracion().paginacion).items

    @staticmethod
    def getCentroByEmail(email):
        return Centro.query.filter(Centro.email == email).first()

    @staticmethod
    def getCentroByAddress(address):
        return Centro.query.filter(Centro.address == address).first()

    @staticmethod   
    def getCentroByPhone(phone):
        return Centro.query.filter(Centro.phone == phone).first()