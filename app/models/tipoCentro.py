from app.db_sqlalchemy import db_sqlalchemy
from app.models.centro import Centro

db = db_sqlalchemy


class TipoCentro(db.Model):
    __tablename__ = 'tipo_centro'
    id = db.Column(db.Integer, primaryKey=True)
    name = db.Column(db.String, unique=True, nullable=False)
    centers = db.relationship('Centro')


