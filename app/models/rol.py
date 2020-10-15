from app.db_sqlalchemy import db_sqlalchemy

db = db_sqlalchemy

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer , primary_key = True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    permisos = db.relationship('Permiso', secondary=permisos, lazy='subquery', backref=db.backref('roles', lazy=True))