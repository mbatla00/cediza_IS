# 🗄️ GUÍA PARA DAOs (Data Access Objects)

## ¿Qué es esta carpeta?
Aquí va **toda la interacción con la base de datos**. Cada clase DAO gestiona
las operaciones CRUD de una tabla. La conexión se gestiona con el **patrón Singleton**
para que solo exista una conexión activa en toda la app.

## Responsable: Sofía

---

## ⚠️ PENDIENTE DE MIGRACIÓN A JDBC

Actualmente la conexión usa `mysql.connector` (Python). En el futuro se migrará
a **JDBC** (Java Database Connectivity). Cuando se haga la migración:

- `database.py` es el único archivo que cambia — el resto de DAOs no se tocan
- Habrá que reemplazar `mysql.connector.connect(...)` por la configuración JDBC correspondiente
- Los métodos de los DAOs seguirán funcionando igual siempre que la nueva conexión
  devuelva cursores con `dictionary=True`

> Hasta entonces, asegúrate de tener instalado `mysql-connector-python` en el entorno.

---

## 🗂️ ARCHIVOS Y CLASES

```
dao/
├── database.py          → Database (Singleton — CREAR PRIMERO)
├── usuario_dao.py       → UsuarioDAO
├── paciente_dao.py      → PacienteDAO, PacPubDAO, PacPriDAO
├── trabajador_dao.py    → TrabajadorDAO, AuxiliarDAO, CoordinadorDAO, EspecialistaDAO
├── otros_dao.py         → FamiliarDAO, ComentarioDAO, SesionDAO
└── cuestionario_dao.py  → CuestionarioDAO, PreguntaDAO, RespuestaDAO
```

---

## 📋 FUNCIONES DE CADA DAO

### UsuarioDAO
| Método | Descripción |
|---|---|
| `get_by_nombreUsuario(nombreUsuario)` | Login — devuelve el objeto del subtipo correcto via factoría (con doble LEFT JOIN a Pacientes y Trabajadores) |
| `get_by_email(email)` | Búsqueda por email |
| `get_by_dni(dni)` | Búsqueda por DNI |
| `create(usuario)` | Inserta en `Usuarios`. El campo email es opcional |
| `update(usuario)` | Actualiza Nombre, email, DNI y password |
| `delete(nombreUsuario)` | Borrado lógico: marca `activo = 0` |

### PacienteDAO / PacPubDAO / PacPriDAO
| Método | Descripción |
|---|---|
| `PacienteDAO.get_all()` | Lista todos los pacientes |
| `PacienteDAO.get_by_nombreUsuario(u)` | Busca un paciente |
| `PacienteDAO.create(paciente)` | Inserta en `Pacientes` |
| `PacienteDAO.delete(nombreUsuario)` | Elimina de `Pacientes` |
| `PacPubDAO.get_by_nombreUsuario(u)` | Busca un paciente público |
| `PacPubDAO.create(pac_pub)` | Inserta en `Pac_pub` |
| `PacPubDAO.update_dias(u, dias)` | Actualiza días ingresado (facturación) |
| `PacPriDAO.get_by_nombreUsuario(u)` | Busca un paciente privado |
| `PacPriDAO.create(pac_pri)` | Inserta en `Pac_pri` |
| `PacPriDAO.update(pac_pri)` | Actualiza IVA, cuenta y horas |

### TrabajadorDAO / AuxiliarDAO / CoordinadorDAO / EspecialistaDAO
| Método | Descripción |
|---|---|
| `TrabajadorDAO.get_all()` | Lista todos los trabajadores |
| `TrabajadorDAO.get_by_nombreUsuario(u)` | Busca un trabajador |
| `TrabajadorDAO.create(trabajador)` | Inserta en `Trabajadores` |
| `TrabajadorDAO.delete(nombreUsuario)` | Elimina de `Trabajadores` |
| `AuxiliarDAO.get_all()` | Lista todos los auxiliares |
| `AuxiliarDAO.get_by_nombreUsuario(u)` | Busca un auxiliar |
| `AuxiliarDAO.create(auxiliar)` | Inserta en `Auxiliares` |
| `AuxiliarDAO.update_horario(u, horario)` | Actualiza el horario |
| `CoordinadorDAO.get_by_nombreUsuario(u)` | Busca un coordinador |
| `CoordinadorDAO.create(coordinador)` | Inserta en `coordinadores` |
| `CoordinadorDAO.update_infoInteres(u, info)` | Actualiza infoInteres |
| `EspecialistaDAO.get_all()` | Lista todos los especialistas |
| `EspecialistaDAO.get_by_nombreUsuario(u)` | Busca un especialista |
| `EspecialistaDAO.create(especialista)` | Inserta en `Especialistas` |
| `EspecialistaDAO.update(especialista)` | Actualiza especialidad y horario |

### FamiliarDAO / ComentarioDAO / SesionDAO
| Método | Descripción |
|---|---|
| `FamiliarDAO.get_by_paciente(u)` | Lista los familiares de un paciente |
| `FamiliarDAO.create(familiar)` | Inserta un familiar |
| `FamiliarDAO.delete(nombre, paciente)` | Elimina un familiar |
| `ComentarioDAO.get_by_paciente(u)` | Lista comentarios de un paciente (más reciente primero) |
| `ComentarioDAO.get_by_trabajador(u)` | Lista comentarios escritos por un trabajador |
| `ComentarioDAO.create(comentario)` | Inserta un comentario |
| `ComentarioDAO.delete(auxiliar, paciente, dia)` | Elimina un comentario por clave compuesta |
| `SesionDAO.get_by_id(id)` | Busca una sesión por ID |
| `SesionDAO.get_by_paciente(u)` | Lista sesiones de un paciente (ordenadas por fecha) |
| `SesionDAO.get_by_especialista(u)` | Lista sesiones de un especialista (ordenadas por fecha) |
| `SesionDAO.create(sesion)` | Inserta una sesión y devuelve el `idSesion` generado |
| `SesionDAO.update(sesion)` | Actualiza una sesión existente |
| `SesionDAO.delete(idSesion)` | Elimina una sesión |

### CuestionarioDAO / PreguntaDAO / RespuestaDAO
| Método | Descripción |
|---|---|
| `CuestionarioDAO.get_all()` | Lista todos los cuestionarios |
| `CuestionarioDAO.get_by_id(id)` | Busca un cuestionario por ID |
| `CuestionarioDAO.create(cuestionario)` | Inserta un cuestionario y devuelve el id generado |
| `CuestionarioDAO.update(cuestionario)` | Actualiza título, tipo y fecha |
| `CuestionarioDAO.delete(id)` | Elimina un cuestionario |
| `PreguntaDAO.get_by_cuestionario(id)` | Lista preguntas de un cuestionario |
| `PreguntaDAO.get_by_id(id)` | Busca una pregunta por ID |
| `PreguntaDAO.create(pregunta)` | Inserta una pregunta y devuelve el id generado |
| `PreguntaDAO.delete(id)` | Elimina una pregunta |
| `RespuestaDAO.get_by_paciente(u)` | Lista respuestas de un paciente (más reciente primero) |
| `RespuestaDAO.get_by_pregunta(id)` | Lista respuestas de una pregunta (más reciente primero) |
| `RespuestaDAO.create(respuesta)` | Inserta una respuesta y devuelve el id generado |
| `RespuestaDAO.delete(id)` | Elimina una respuesta |

---

## 💡 EJEMPLO DE USO

```python
# --- Login ---
from app.dao.usuario_dao import UsuarioDAO

usuario = UsuarioDAO.get_by_nombreUsuario('mariagarcia')
if usuario and usuario.password == password_introducida:
    print(f"Bienvenido {usuario.nombre}")   # objeto ya del subtipo correcto


# --- Crear un paciente público (insert en cascada) ---
from app.dao.usuario_dao import UsuarioDAO
from app.dao.paciente_dao import PacienteDAO, PacPubDAO
from app.factories.usuario_factory import UsuarioFactory

datos = {
    'Rol': 'paciente',
    'Tipo': 'publico',
    'Nombre': 'Maria Garcia Lopez',
    'DNI': '12345678A',
    'password': '1234',
    'Dias_ingresado': 10
}

pac = UsuarioFactory.crear(datos)   # genera nombreUsuario automáticamente

UsuarioDAO.create(pac)              # 1. inserta en Usuarios
PacienteDAO.create(pac)             # 2. inserta en Pacientes
PacPubDAO.create(pac)               # 3. inserta en Pac_pub


# --- Crear un trabajador (insert en cascada) ---
from app.dao.usuario_dao import UsuarioDAO
from app.dao.trabajador_dao import TrabajadorDAO, AuxiliarDAO
from app.factories.usuario_factory import UsuarioFactory

datos = {
    'Rol': 'trabajador',
    'Tipo': 'auxiliar',
    'Nombre': 'Ana Garcia Lopez',
    'DNI': '87654321X',
    'password': 'trab123',
    'Horario': 'Mañana'
}

trab = UsuarioFactory.crear(datos)

UsuarioDAO.create(trab)             # 1. inserta en Usuarios
TrabajadorDAO.create(trab)          # 2. inserta en Trabajadores
AuxiliarDAO.create(trab)            # 3. inserta en Auxiliares


# --- Borrar un usuario (borrado lógico) ---
UsuarioDAO.delete('GarciaLopezMaria')   # marca activo = 0, no elimina el registro
```

---

## 🛡️ REGLAS DE ORO

- **NUNCA** concatenes strings en SQL — usa siempre parámetros: `cursor.execute(sql, (val1, val2))`
- **SIEMPRE** cierra el cursor en `finally`
- **NUNCA** cierres la conexión — la gestiona el Singleton
- Usa `conn.rollback()` si hay error en INSERT / UPDATE / DELETE
- Los inserts de pacientes y trabajadores son **siempre en cascada** — el orden importa:
  `Usuarios` → `Pacientes`/`Trabajadores` → tabla específica
- Esa cascada la gestiona el **controlador**, no el DAO
- El borrado de usuarios es **lógico** (`activo = 0`) — nunca se elimina el registro

---

## 📝 CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR

- `get_by_nombreUsuario` hace doble LEFT JOIN con `Pacientes` y `Trabajadores` para obtener el `Tipo` y construir el objeto del subtipo correcto
- `create` usa `getattr(usuario, 'email', None)` para que el campo email sea opcional
- `delete` usa borrado lógico (`activo = 0`) en lugar de borrado físico
- `update` ahora actualiza también el campo `email`
- El campo `contraseña` en BD se renombró a `password` para evitar problemas de codificación
- Añadidos `CuestionarioDAO`, `PreguntaDAO` y `RespuestaDAO` para las nuevas tablas