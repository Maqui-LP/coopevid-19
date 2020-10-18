from app.db_sqlalchemy import db_sqlalchemy

db = db_sqlalchemy

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer , primary_key = True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    contacto = db.Column(db.String(255), nullable=False)
    mantenimiento = db.Column(db.Boolean, nullable=False)
    paginacion = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        self.titulo = data["titulo"]
        self.descripcion = data["descripcion"]
        self.contacto = data["contacto"]
        self.mantenimiento = data["mantenimiento"]
        self.paginacion = data["paginacion"]
    
    @staticmethod
    def getConfiguracion():
        return Configuracion.query.filter().order_by(Configuracion.id.desc()).first()

    @staticmethod
    def updateConfiguracion(data):
        config = Configuracion(data)
        db.session.add(config)
        db.session.commit()

    @staticmethod
    def getStateOfSite():
        
        return Configuracion.getConfiguracion().mantenimiento
        
        