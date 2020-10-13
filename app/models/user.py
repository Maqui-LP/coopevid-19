from app.db_sqlalchemy import db_sqlalchemy
from flask import Flask, request, jsonify
from datetime import datetime

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
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    #roles = db.relationship('Rol', secondary=roles, lazy='subquery',
     #   backref=db.backref('users', lazy=True)
    #)

    #@classmethod
    #def all(cls):
        #sql = "SELECT * FROM users"
        #cursor = conn.cursor()
        #cursor.execute(sql)
        
    def __init__(self, data):
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.activo = data['activo']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        hoy = datetime.now()
        #.strftime("%m/%d/%Y, %H:%M:%S")
        self.created_at = hoy
        self.updated_at = hoy
   
    #@classmethod
    #def find_by_email_and_pass(cls, conn, email, password):
     #   sql = """
      #      SELECT * FROM users AS u
       #     WHERE u.email = %s AND u.password = %s
        #"""

        #cursor = conn.cursor()
        #cursor.execute(sql, (email, password))

        #return cursor.fetchone()

