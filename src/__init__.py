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
from .config import Config
from pathlib import Path


def create_app():
    """Crea y configura la aplicación Flask"""

    src_path = Path(__file__).parent.resolve()
    vista_path = src_path / 'vista'

    app = Flask(__name__,
        template_folder=str(vista_path),
        static_folder=str(vista_path / 'static'))

    # Cargar configuración desde la clase Config
    app.config.from_object(Config)

    # Registrar el blueprint de autenticación (login, logout, seguridad)
    from src.controlador.auth import auth_bp
    app.register_blueprint(auth_bp)


    from src.controlador.admin import admin_bp
    app.register_blueprint(admin_bp)

    from src.controlador.trabajador import trabajador_bp
    app.register_blueprint(trabajador_bp)

    # Los demás blueprints se registrarán cuando sus controladores existan
    # Esto evita errores si alguien no ha creado aún su parte

    from src.controlador.paciente import paciente_bp
    app.register_blueprint(paciente_bp)

    return app