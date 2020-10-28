from app.db_sqlalchemy import db_sqlalchemy
from sqlalchemy.dialects.mysql import TIME
db = db_sqlalchemy

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
    

    #TODO: agregar el protocolo con formato PDF y el tema del municipio 
    #el municipio no se si tenemos que crear una clase municipio en base 
    #a la api de la catedra o solo poner el String con el nombre