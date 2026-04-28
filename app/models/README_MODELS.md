# 📦 GUÍA PARA MODELOS (Value Objects - VO)

## ¿Qué es esta carpeta?
Aquí van las clases que representan las **tablas de la base de datos**.
Son clases simples: solo atributos, getters, setters y método `to_dict()`.

---

## 📝 PLANTILLA PARA CADA MODELO

```python
# Ejemplo: usuario.py

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None, rol=None, 
                 fecha_registro=None, activo=True):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._password = password
        self._rol = rol          # 'admin', 'trabajador', 'paciente'
        self._fecha_registro = fecha_registro
        self._activo = activo
    
    # Getters
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password
    
    @property
    def rol(self):
        return self._rol
    
    # Setters
    @id.setter
    def id(self, value):
        self._id = value
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @password.setter
    def password(self, value):
        self._password = value
    
    @rol.setter
    def rol(self, value):
        self._rol = value
    
    def to_dict(self):
        """Convierte el objeto a diccionario (útil para JSON)"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol
        }
```

## CHECKLIST DE ARCHIVOS A CREAR

- **usuario.py** - Clase Usuario (base para todos los roles)
- **paciente.py** - Hereda de Usuario + DNI, fecha_nacimiento, diagnostico, foto
- **trabajador.py** - Hereda de Usuario + especialidad
- **contacto_emergencia.py** - Contactos de emergencia asociados a un paciente
- **nota.py** - Notas libres escritas por trabajadores
- **evaluacion.py** - Evaluaciones rápidas con puntuaciones (1-5)
- **respuesta.py** - Respuestas de pacientes a cuestionarios diarios
- **pregunta_diaria.py** - Preguntas predefinidas del cuestionario
- **informe.py** - Metadatos de informes PDF generados

## 🔗 RELACIONES ENTRE CLASES (según el Diagrama de Dominio)

Usuario (base)
├── Paciente (hereda de Usuario)
│   ├── ContactoEmergencia (N contactos por paciente)
│   ├── NotaLibre (N notas por paciente)
│   ├── EvaluacionProfesional (N evaluaciones por paciente)
│   └── Respuesta (N respuestas por paciente)
└── Trabajador (hereda de Usuario)
    ├── NotaLibre (1 trabajador escribe N notas)
    └── EvaluacionProfesional (1 trabajador hace N evaluaciones)

## ⚠️ IMPORTANTE

- **NO incluyáis lógica de base de datos aquí** (eso va en `dao/`)
- **Todos los atributos deben ser privados** (con `_`) y usar `@property`
- **El método `to_dict()` es obligatorio** para enviar datos a las vistas