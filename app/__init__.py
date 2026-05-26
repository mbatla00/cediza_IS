"""
Fábrica de la aplicación Flask.

Este archivo:
- Crea la aplicación Flask con la función create_app()
- Carga la configuración desde config.py
- Registra los blueprints (controladores) de cada módulo
- Es el punto central que conecta todas las piezas del proyecto

Un blueprint es un "mini-aplicación" que agrupa rutas relacionadas.
Ejemplo: auth_bp agrupa login, logout y protección de rutas.
"""
from flask import Flask
from app.config import Config


def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)

    # Cargar configuración desde la clase Config
    app.config.from_object(Config)

    # Registrar el blueprint de autenticación (login, logout, seguridad)
    from app.controllers.auth import auth_bp
    app.register_blueprint(auth_bp)


    from app.controllers.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.controllers.trabajador import trabajador_bp
    app.register_blueprint(trabajador_bp)

    # Los demás blueprints se registrarán cuando sus controladores existan
    # Esto evita errores si alguien no ha creado aún su parte

    from app.controllers.paciente import paciente_bp
    app.register_blueprint(paciente_bp)

    return app