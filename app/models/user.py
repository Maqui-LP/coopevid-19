from app.db_sqlalchemy import db_sqlalchemy

db = db_sqlalchemy

roles = db.Table('usuario_tiene_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)
    create_at = db.Column(db.DateTime, nullable=False)
    roles = db.relationship('Rol', secondary=roles, lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    #@classmethod
    #def all(cls):
        #sql = "SELECT * FROM users"
        #cursor = conn.cursor()
        #cursor.execute(sql)
        
        

    @classmethod
    def create(cls, conn, data):
        sql = """
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """

        #cursor = conn.cursor()
        #cursor.execute(sql, list(data.values()))
        #conn.commit()

        #return True

    @classmethod
    def find_by_email_and_pass(cls, conn, email, password):
        sql = """
            SELECT * FROM users AS u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()

