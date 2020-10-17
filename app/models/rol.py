from app.db_sqlalchemy import db_sqlalchemy
from app.models.permiso import Permiso

db = db_sqlalchemy

rol_tiene_permiso = db.Table('rol_tiene_permiso',
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id')),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'))
)

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer , primary_key = True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    permisos = db.relationship('Permiso', 
                                secondary=rol_tiene_permiso)