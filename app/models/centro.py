from app.db_sqlalchemy import db_sqlalchemy
from sqlalchemy.dialects.mysql import TIME
from app.models.turno import Turno
db = db_sqlalchemy

tipo_centro = db.Table('tipo_centro',
    db.Column('id', db.Integer, db.ForeignKey('centros.type_id'))
)

class Centro(db.Model):
    __tablename__ = 'centros'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone= db.Column(db.String(255),unique=True,nullable=False)
    openHour= db.Column(TIME(), unique=False, nullable=False)
    closeHour= db.Column(TIME(), unique=False, nullable=False)
    type_id= db.Column(db.Integer, db.ForeignKey('tipo_centro.id'), nullable=False)
    web= db.Column(db.String, unique=False , nullable=False)
    status = db.Column(db.Boolean,nullable=False)
    address = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    turnos = db.relationship('Turno', backref="centros")

    #TODO: agregar el protocolo con formato PDF y el tema del municipio 
    #el municipio no se si tenemos que crear una clase municipio en base 
    #a la api de la catedra o solo poner el String con el nombre

    def __init__(self, data):
        self.name = data['name']
        self.phone = data['phone']
        self.openHour = data['openHour']
        self.closeHour = data['closeHour']
        self.type_id = data['type_id']
        self.web = data['web']
        self.status = data['status']
        self.address = data['address']
        self.lat = data['lat']
        self.long = data['long']

    @staticmethod
    def getAll():
        return Centro.query.all()
    
    @staticmethod
    def getCentroById(centro_id):
        return Centro.query.filter(Centro.id == centro_id).first()