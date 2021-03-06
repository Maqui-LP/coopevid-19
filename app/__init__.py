from os import path, environ, urandom
from flask import Flask, render_template, g, session
from flask_session import Session

from app.db_sqlalchemy import db_sqlalchemy
from config import config
from app import db
from app.resources import issue
from app.resources import user
from app.resources import centro
from app.resources import turno
from app.resources import auth
from app.resources import rol
from app.resources import configuracion
from app.resources.api import centro as centroApi
from app.models.configuracion import Configuracion

from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import granted
from app.helpers import config as config_helper
from app.csrf import app_csrf
from flask_cors import CORS
#from flask_bootstrap import Bootstrap


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    app_csrf.init_app(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, headers="Content-Type")
    #cors = CORS(app, resources={r"/api/centros/all": {"origins": "*"}})
    #app.config['CORS_HEADERS'] = 'Content-Type'

    #Definicion de path de archivos estaticos
    #app.config['CENTROS_PDF'] = '/media/pdfs'

    SECRET_KEY = urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    #Bootstrap
    #Bootstrap(app)
    
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    #SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+app.config["DB_USER"]+":"+app.config["DB_PASS"]+"@"+app.config["DB_HOST"]+"/"+app.config["DB_NAME"]
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_sqlalchemy.init_app(app)

    #db_sqlalchemy.create_all();
    #db = SQLAlchemy()
    #db.init_app(app)
    #db_sqlalchemy.init_app(app)
    # db_sqlalchemy.create_all()
    with app.app_context():
        db_sqlalchemy.create_all()
    db_sqlalchemy.session.configure(autoflush=False)



    #with app.app_context():
     #   db.create_all()

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated, is_granted=granted.granted, getConfig=config_helper.getConfig)
    app.config["TEMPLATES_AUTO_RELOAD"]=True

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Consultas
    app.add_url_rule("/consultas", "issue_index", issue.index)
    app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/administrarRoles", "user_roles", user.roles)
    app.add_url_rule("/usuarios/administrarRoles", "modificar_roles", user.modificarRoles, methods=["POST"])    
    app.add_url_rule("/usuarios/delete", "user_delete", user.delete, methods=["POST"])
    app.add_url_rule("/usuarios/update", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/editar", "user_edit", user.edit)
    app.add_url_rule("/usuarios/perfil", "user_perfil", user.perfil)
    app.add_url_rule("/usuarios/perfil", "user_perfilUpdate", user.perfilUpdate, methods=["POST"])
    app.add_url_rule("/usuarios/toogleUser", "toogle_user_activity", user.toogleUserActivity, methods=["POST"])
    #rutas para busqueda de usuarios
    app.add_url_rule("/usuarios/search", "search_users_page", user.searchUserPage)
    app.add_url_rule("/usuarios/search/list", "search_users", user.searchUsers)

    #Rutas para centros
    app.add_url_rule("/centros", "centro_index", centro.index)
    app.add_url_rule("/centros", "centro_create", centro.create, methods=["POST"])
    app.add_url_rule("/centros/nuevo", "centro_new", centro.new)
    app.add_url_rule("/centros/delete", "centro_delete", centro.delete , methods=["POST"])
    app.add_url_rule("/centro/detalle", "centro_detalle", centro.detalle)
    app.add_url_rule("/centro/editar", "centro_edit", centro.edit)
    app.add_url_rule("/centro/toggleCentro", "toggle_publicacion", centro.togglePublicacion, methods=["POST"])
    app.add_url_rule("/centro/statusCreate", "definir_status_create", centro.definirStatusCreate, methods=["POST"])
    app.add_url_rule("/centro/toggleCentroAprobacion", "toggle_aprobacion", centro.toggleAprobacion, methods=["POST"])
    #ruta para enviar cambios
    app.add_url_rule("/centro/update", "centro_update", centro.update, methods=["POST"])
    #Rutas para busqueda de Centros
    app.add_url_rule("/centros/search", "search_centros_page", centro.searchCentrosPage)
    app.add_url_rule("/centros/search/list", "search_centro", centro.searchCentros)

    # Rutas para Turnos 
    app.add_url_rule("/turnos", "turno_index", turno.index)
    app.add_url_rule("/turnos", "turno_create", turno.create, methods=["POST"])
    app.add_url_rule("/turnos/nuevo", "turno_new", turno.new)
    app.add_url_rule("/turnos/delete", "turno_delete", turno.delete , methods=["POST"])
    app.add_url_rule("/turnos/update", "turno_update", turno.update, methods=["POST"])
    app.add_url_rule("/turnos/editar", "turno_edit", turno.edit)
    #ruta para busqueda de turnos
    app.add_url_rule("/turnos/search", "search_turnos_page", turno.searchTurnoPage)
    app.add_url_rule("/turnos/search/list", "search_turnos", turno.searchTurnos)

    # Rutas de Roles
    app.add_url_rule("/roles", "roles_index", rol.index)
    app.add_url_rule("/roles", "roles_create", rol.create, methods=["POST"])
    app.add_url_rule("/roles/nuevo", "roles_new", rol.new)

    # Rutas para administrar el sistema
    app.add_url_rule("/configuracion", "configuracion_form", configuracion.form )
    app.add_url_rule("/configuracion", "configuracion_update", configuracion.update , methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        if Configuracion.getStateOfSite():
            return render_template("mantenimiento.html")
        else:    
            return render_template("home.html")


    # Rutas de API-rest
    #app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(403, handler.forbbiden_error)
    app.register_error_handler(500, handler.internal_server_error)


    #API REST routes
    ##centros
    app.add_url_rule("/api/centros", "centro_api_index", centroApi.index, methods=["GET"])
    app.add_url_rule("/api/centros/<id>", "centro_id_api_index", centroApi.getById, methods=["GET"])
    app.add_url_rule("/api/centros", "centro_api_create", centroApi.create, methods=["POST"])
    app.add_url_rule("/api/centros/<id>/reserva", "centro_api_reserva", centroApi.reserva, methods=["POST"])
    app.add_url_rule("/api/centros/all", "centro_api_get_all_not_paginated", centroApi.get_all_not_paginated, methods=["GET"])
    ##turnos
    app.add_url_rule("/api/centros/<id>/turnos_disponibles", "centro_api_turnos", centroApi.getTurnoByFecha, methods=["GET"])
    ##estadisticas
    app.add_url_rule("/api/centros/estadisticas/porTipos", "centro_api_get_estadisticas_tipo_centro", centroApi.get_estadisticas_tipo_centro, methods=["GET"])

    app.add_url_rule("/api/centros/estadisticas/por_municipio", "centro_api_get_estadisticas_por_municipio", centroApi.get_estadisticas_centros_por_municipio, methods=["GET"])

    app.add_url_rule("/api/centros/estadisticas/turnos", "centro_api_get_estadisticas_turnos", centroApi.get_estadisticas_turnos, methods=["GET"])

    # Retornar la instancia de app configurada
    return app
