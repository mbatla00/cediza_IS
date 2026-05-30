"""
Punto de entrada de la aplicación CEDIZA.
Ejecutar con: python run.py

Este archivo es el interruptor de encendido del proyecto.
- Importa la fábrica de la app desde app/__init__.py
- Arranca el servidor Flask en modo desarrollo
- host='0.0.0.0' permite que tablets/móviles en la misma WiFi se conecten
- debug=True muestra errores detallados y se reinicia al guardar cambios
"""
from src import create_app

app = create_app()

if __name__ == '__main__':
    print("\n🚀 CEDIZA iniciando...")
    print("📱 http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)