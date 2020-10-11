from app.db_sqlalchemy import db_sqlalchemy
db = db_sqlalchemy

class Queso(db.Model):
    __tablename__= 'quesos'
    id =  db.Column(db.Integer, primary_key=True)
    olor = db.Column(db.String(255))

    def __repr__(self):
        return '<Queso {0} {1}>'.format(self.id,
                                               self.olor)

    def __init__(self,data):
        self.olor = data["olor"]

    @classmethod
    def create(cls, data):
        queso = Queso(data)
        db.session.add(queso)
        db.session.commit()
        