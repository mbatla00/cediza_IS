# 🗄️ GUÍA PARA DAOs (Data Access Objects)

## ¿Qué es esta carpeta?
Aquí va **TODA la interacción con MySQL**. Cada clase DAO maneja las operaciones
CRUD de una tabla. Implementamos el **patrón Singleton** para la conexión.

## Responsable: Sofía

---

## 🎯 PRIMER ARCHIVO A CREAR: database.py

```python
"""Conexión a MySQL con patrón Singleton"""
import mysql.connector
from mysql.connector import Error
from app.config import Config

class Database:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    pool_name="cediza_pool",
                    pool_size=5
                )
                print("✅ Conexión a MySQL establecida")
            except Error as e:
                print(f"❌ Error de conexión: {e}")
                return None
        return self._connection
    
    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔌 Conexión cerrada")
```

## 📝 PLANTILLA PARA CADA DAO

```python
# Ejemplo: usuario_dao.py
from app.dao.database import Database
from app.models.usuario import Usuario
from mysql.connector import Error

class UsuarioDAO:
    
    @staticmethod
    def get_by_email(email):
        """Busca un usuario por su email (usado en login)"""
        db = Database()
        conn = db.get_connection()
        
        if conn is None:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
            row = cursor.fetchone()
            if row:
                return Usuario(**row)
            return None
        except Error as e:
            print(f"Error en get_by_email: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def create(usuario):
        """Inserta un nuevo usuario"""
        db = Database()
        conn = db.get_connection()
        
        cursor = conn.cursor()
        try:
            sql = """INSERT INTO Usuario (nombre, email, password, rol)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (usuario.nombre, usuario.email, 
                                usuario.password, usuario.rol))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al crear usuario: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def update(usuario):
        """Actualiza los datos de un usuario"""
        # Implementar UPDATE
        pass
    
    @staticmethod
    def delete(id_usuario):
        """Marca un usuario como inactivo (borrado lógico)"""
        # Implementar DELETE lógico (activo = 0)
        pass
```

## ✅ CHECKLIST DE DAOs A CREAR

- **database.py** - Clase Database con patrón Singleton (OBLIGATORIO PRIMERO)
- **usuario_dao.py** - CRUD de usuarios + get_by_email para login
- **paciente_dao.py** - CRUD de pacientes + búsqueda por DNI
- **trabajador_dao.py** - CRUD de trabajadores
- **contacto_emergencia_dao.py** - CRUD de contactos de emergencia
- **nota_dao.py** - Guardar y recuperar notas libres
- **evaluacion_dao.py** - Guardar y recuperar evaluaciones rápidas
- **respuesta_dao.py** - Guardar respuestas de cuestionarios
- **pregunta_dao.py** - Obtener preguntas diarias

## 🛡️ REGLAS DE ORO PARA DAOs

- **NUNCA** concatenar strings en SQL (riesgo de SQL Injection)
- **SIEMPRE** usar parámetros: `cursor.execute(sql, (valor1, valor2))`
- **SIEMPRE** cerrar el cursor en `finally`
- **NUNCA** cerrar la conexión (la gestiona el Singleton)
- Usar `conn.rollback()` si hay error en INSERT/UPDATE/DELETE

