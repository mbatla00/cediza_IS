"""
Configuración central de la aplicación.

Este archivo:
- Carga las variables del archivo .env (que NO se sube a GitHub)
- Define la clase Config con todos los ajustes del sistema
- Si no encuentra .env, usa valores por defecto para desarrollo

Las variables de .env son:
- SECRET_KEY: clave para cifrar cookies de sesión
- MYSQL_*: datos de conexión a la base de datos MySQL
"""
import os
from dotenv import load_dotenv

# Carga el archivo .env (datos privados de cada desarrollador)
load_dotenv()


class Config:
    """Clase con todas las variables de configuración de Flask"""

    # Clave secreta para firmar cookies de sesión
    # La toma de .env o usa un valor por defecto para desarrollo
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-temporal-cediza'

    # Datos de conexión a MySQL
    # Cada desarrollador tiene los suyos en su archivo .env
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'db_cediza'