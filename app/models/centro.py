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
    municipio_id = db.Column(db.Integer)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    file_name = db.Column(db.String, nullable=True)
    status_create = db.Column(db.String, nullable=False)
    turnos = db.relationship('Turno', cascade="all, delete-orphan")

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
        self.municipio_id = data['municipio_id']
        self.lat = data['lat']
        self.long = data['long']
        self.status_create = data['status_create']
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
    def getAllByNameStatusCreate(name, selected_statuses):
        return Centro.query.filter(Centro.name.like(name), Centro.status_create.in_(selected_statuses))

    @staticmethod
    def getAllByNameStatusCreatePaginado(numero_pagina, name, selected_statuses):
        return Centro.query.filter(Centro.name.like(name), Centro.status_create.in_(selected_statuses)).paginate(page=numero_pagina, per_page=Configuracion.getConfiguracion().paginacion).items

    @staticmethod
    def getAllByName(name):
        return Centro.query.filter(Centro.name.like(name))

    @staticmethod
    def get_all_published_centers():
        return Centro.query.filter(Centro.status == True)

    @staticmethod
    def getCentroByEmail(email):
        return Centro.query.filter(Centro.email == email).first()

    @staticmethod
    def getCentroByAddress(address):
        return Centro.query.filter(Centro.address == address).first()

    @staticmethod   
    def getCentroByPhone(phone):
        return Centro.query.filter(Centro.phone == phone).first()

    @staticmethod
    def getCentroByName(name):
        return Centro.query.filter(Centro.name == name).first()

    @staticmethod
    def updateCentro(centro_id, data):
        data.pop('csrf_token')
        Centro.query.filter(Centro.id == centro_id).update(data)

    @staticmethod
    def togglePublicacion(centro_id):
        estado = Centro.query.filter(Centro.id == centro_id).first().status
        Centro.query.filter(Centro.id == centro_id).update({'status': not estado})

    @staticmethod
    def definirStatusCreate(centro_id, status):
        Centro.query.filter(Centro.id == centro_id).update({'status_create': status})

    @staticmethod
    def getStatusesList():
        return ['ACEPTADO', 'RECHAZADO', 'PENDIENTE']

    @staticmethod
    def toggleAprobacion(centro_id):
        estado = Centro.query.filter(Centro.id == centro_id).first().status_create
        if estado == "ACEPTADO":
            nuevo_estado = "RECHAZADO"
            Centro.query.filter(Centro.id == centro_id).update({'status_create': nuevo_estado})
            Centro.query.filter(Centro.id == centro_id).update({'status': False})
        else:
            nuevo_estado = "ACEPTADO"
            Centro.query.filter(Centro.id == centro_id).update({'status_create': nuevo_estado})
    
    @staticmethod
    def getStatusAprobacion(centro_id):
        return Centro.query.filter(Centro.id == centro_id).first().status_create        

    @staticmethod
    def get_all_comida():
        return Centro.query.filter(Centro.type_id == 2, Centro.status == True).count()

    @staticmethod
    def get_all_ropa():
        return Centro.query.filter(Centro.type_id == 1, Centro.status == True).count()

    @staticmethod
    def get_all_muebles():
        return Centro.query.filter(Centro.type_id == 3, Centro.status == True).count()

    @staticmethod
    def get_all_higiene_hogar():
        return Centro.query.filter(Centro.type_id == 5, Centro.status == True).count()

    @staticmethod
    def get_all_higiene_personal():
        return Centro.query.filter(Centro.type_id == 4, Centro.status == True).count()

    @staticmethod
    def get_quantity_for_municipio_id(muni_id):
        return Centro.query.filter(Centro.municipio_id == muni_id).count()
