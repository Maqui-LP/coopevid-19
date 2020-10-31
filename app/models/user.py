from app.db_sqlalchemy import db_sqlalchemy
from flask import Flask, request, jsonify
from datetime import datetime
from app.models.rol import Rol
from app.models.configuracion import Configuracion
from app.models.turno import Turno

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
    turnos = db.relationship('Turno', backref="users")


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
    def getUserByUsername( username):
        return User.query.filter(User.username == username).first()
    
    @staticmethod
    def getUserByEmail( email):
        return User.query.filter(User.email == email).first()
    
    @staticmethod
    def getUserById( user_id):
        return User.query.filter(User.id == user_id).first()

    @staticmethod
    def updateUser(user_id, data):
        User.query.filter(User.id == user_id).update(data)

    @staticmethod
    def toogleUsrActivity(user_id):
        estado = User.query.filter(User.id == user_id).first().activo
        User.query.filter(User.id == user_id).update({'activo':not estado}, synchronize_session = False)
        
    @staticmethod
    def setRoles(user_id, data):
        user = User.getUserById(user_id)
        user.roles = list()
        for each in data:
            rol = Rol.query.filter(Rol.nombre == str(each)).first()
            if rol not in user.roles:
                user.roles.append(rol)

    @staticmethod
    def getByNameLastNameAndState(nombre, apellido, estado):
        return User.query.filter(User.first_name.like(nombre), User.first_name.like(nombre), User.activo == estado)

    @staticmethod
    def getAllPaginado(numero_pagina):
        return User.query.paginate(page=numero_pagina, per_page=Configuracion.getConfiguracion().paginacion).items
        