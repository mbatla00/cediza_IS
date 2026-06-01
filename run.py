"""
PUNTO DE ENTRADA DE LA APLICACIÓN CEDIZA
Ejecutar con: python run.py

Este archivo es el interruptor de encendido del proyecto.
NO USA FLASK - Es una aplicación de escritorio con PySide6.

Flujo:
1. Crea la aplicación Qt (la ventana principal)
2. Inicializa el controlador de autenticación
3. Muestra la ventana de login
4. Ejecuta el bucle de eventos de Qt
"""
import sys
import os

# Añadir src al path para poder importar correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.controlador import AuthController
from src.vista import VentanaLogin

# Los controladores los importamos de src.controlador
from src.controlador import AuthController
from src.vista import VentanaLogin  # La vista la hace tu compañero


def main():
    """Función principal que inicia la aplicación"""
    
    print("\n" + "="*50)
    print("CEDIZA - Centro de Día")
    print("Aplicación de escritorio - Modo desarrollo")
    print("="*50 + "\n")
    
    # 1. Crear la aplicación Qt (SOLO UNA VEZ en toda la app)
    app = QApplication(sys.argv)
    
    # Configurar estilo moderno (opcional)
    app.setStyle('Fusion')
    
    # 2. Crear el controlador de autenticación
    #    Este controlador gestiona login/logout y NO toca la BD directamente
    auth_controller = AuthController()
    
    # 3. Crear la ventana de login (la vista)
    #    La ventana recibe el controlador para poder llamar a login()
    ventana_login = VentanaLogin(auth_controller)
    ventana_login.show()
    
    print("Aplicación iniciada correctamente")
    print("Ventana de login abierta\n")
    
    # 4. Ejecutar el bucle de eventos de Qt
    #    Esto mantiene la app funcionando hasta que se cierre la ventana
    sys.exit(app.exec())


if __name__ == '__main__':
    main()