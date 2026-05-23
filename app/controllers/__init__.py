from flask import Flask
import os

def create_app():
    # Creamos la aplicación
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'clave_secreta_desarrollo_cediza'

    # Conectamos el trabajo de (auth) y (paciente)
    from app.controllers.auth import auth_bp
    from app.controllers.paciente import paciente_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(paciente_bp)
    
    return app

# Inicializamos
app = create_app()