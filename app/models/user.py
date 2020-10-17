from app.db_sqlalchemy import db_sqlalchemy
from flask import Flask, request, jsonify
from datetime import datetime
from app.models.rol import Rol

db = db_sqlalchemy

usuario_tiene_rol = db.Table('usuario_tiene_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'))
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
    roles = db.relationship('Rol',
                            secondary=usuario_tiene_rol)


    def __init__(self, data):
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.activo = data['activo']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        hoy = datetime.now()
        self.created_at = hoy
        self.updated_at = hoy

    def getPermisos(self):
        permisos = set()

        for rol in self.roles:
            for perm in rol.permisos:
                permisos.add(perm.nombre)

        return permisos
    @staticmethod
    def getAll():
        users = User.query.all()

        return users

    @staticmethod
    def getUserByUsername( data):
        return User.query.filter(User.username == data.get("username")).first()
    
    @staticmethod
    def getUserByEmail( data):
        return User.query.filter(User.email == data.get("email")).first()
    
    @staticmethod
    def getUserById( user_id):
        return User.query.filter(User.id == user_id).first()

    @staticmethod
    def updateUser(user_id, data):
        User.query.filter(User.id == user_id).update(data)