# test.py
from app.dao import Database, UsuarioDAO, PacienteDAO, PacPubDAO
from app.factories import UsuarioFactory

# 1) Probar conexión
db = Database()
conn = db.get_connection()
print("Conexión:", "✅ OK" if conn else "❌ FALLO")

# 2) Probar factoría
datos = {
    'Rol': 'paciente',
    'Tipo': 'publico',
    'Nombre': 'Maria Garcia Lopez',
    'DNI': '12345678A',
    'contraseña': '1234',
    'Dias_ingresado': 10
}
pac = UsuarioFactory.crear(datos)
print("Factoría:", pac)

# 3) Probar insert en cascada
UsuarioDAO.create(pac)
PacienteDAO.create(pac)
PacPubDAO.create(pac)
print("Insert:", "✅ OK")

# 4) Probar recuperación
recuperado = UsuarioDAO.get_by_nombreUsuario(pac.nombreUsuario)
print("Select:", recuperado)