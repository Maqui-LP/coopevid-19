from app.db_sqlalchemy import db_sqlalchemy

db = db_sqlalchemy

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer , primary_key = True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)