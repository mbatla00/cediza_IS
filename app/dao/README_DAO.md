# 🗄️ GUÍA PARA DAOs (Data Access Objects)

## ¿Qué es esta carpeta?
Aquí va **toda la interacción con la base de datos**. Cada clase DAO gestiona
las operaciones CRUD de una tabla. La conexión se gestiona con el **patrón Singleton**
para que solo exista una conexión activa en toda la app.

## Responsable: Sofía

---

## ✅ CONEXIÓN JDBC (MIGRADO)

El proyecto utiliza **JayDeBeApi + JDBC** para conectar con la base de datos MySQL.

### Instalación

```bash
pip install -r requirements.txt

---

## 🗂️ ARCHIVOS Y CLASES

```
dao/
├── database.py          → Database (Singleton — CREAR PRIMERO)
├── usuario_dao.py       → UsuarioDAO
├── paciente_dao.py      → PacienteDAO, PacPubDAO, PacPriDAO
├── trabajador_dao.py    → TrabajadorDAO, AuxiliarDAO, CoordinadorDAO, EspecialistaDAO
├── otros_dao.py         → FamiliarDAO, ComentarioDAO, SesionDAO
├── cuestionario_dao.py  → CuestionarioDAO, PreguntaDAO, RespuestaDAO
└── eval_inf_fac_dao.py  → EvaluacionProfesionalDAO, InformeDAO, FacturaDAO
└── admin_dao.py         → AdministradorDAO
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
| `update(usuario)` | Actualiza Nombre, apellidos, email, DNI y password |
| `delete(nombreUsuario)` | Borrado lógico: marca `activo = 0` |

### PacienteDAO / PacPubDAO / PacPriDAO
| Método | Descripción |
|---|---|
| `PacienteDAO.get_all()` | Lista todos los pacientes |
| `PacienteDAO.get_by_nombreUsuario(u)` | Busca un paciente |
| `PacienteDAO.create(paciente)` | Inserta en `Pacientes` (incluye fechaNacimiento, foto, diagnostico, tipoAsistencia) |
| `PacienteDAO.update(paciente)` | Actualiza los campos de `Pacientes` |
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

### AdministradorDAO / EvaluacionProfesionalDAO / InformeDAO / FacturaDAO
| Método | Descripción |
|---|---|
| `AdministradorDAO.get_by_nombreUsuario(u)` | Busca un administrador |
| `AdministradorDAO.create(admin)` | Inserta en `Administrador`. Llama DESPUÉS de insertar en `Usuarios` |
| `AdministradorDAO.delete(nombreUsuario)` | Elimina de `Administrador` |
| `EvaluacionProfesionalDAO.get_by_id(id)` | Busca una evaluación por ID |
| `EvaluacionProfesionalDAO.get_by_paciente(u)` | Lista evaluaciones de un paciente (más reciente primero) |
| `EvaluacionProfesionalDAO.get_by_trabajador(u)` | Lista evaluaciones hechas por un trabajador |
| `EvaluacionProfesionalDAO.create(evaluacion)` | Inserta una evaluación y devuelve el id generado |
| `EvaluacionProfesionalDAO.update(evaluacion)` | Actualiza movilidad, estadoEmocional, apetito y observaciones |
| `EvaluacionProfesionalDAO.delete(id)` | Elimina una evaluación |
| `InformeDAO.get_by_referencia(ref)` | Busca un informe por referencia |
| `InformeDAO.get_by_paciente(u)` | Lista informes de un paciente (más reciente primero) |
| `InformeDAO.create(informe)` | Inserta un informe |
| `InformeDAO.delete(ref)` | Elimina un informe |
| `FacturaDAO.get_by_codigo(cod)` | Busca una factura por código |
| `FacturaDAO.get_by_paciente(u)` | Lista facturas de un paciente (más reciente primero) |
| `FacturaDAO.get_by_administrador(u)` | Lista facturas gestionadas por un administrador |
| `FacturaDAO.create(factura)` | Inserta una factura |
| `FacturaDAO.update_estado(cod, estado)` | Actualiza el estado de pago |
| `FacturaDAO.update_importe(cod, importe)` | Actualiza el importe total |
| `FacturaDAO.delete(cod)` | Elimina una factura |

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
    'Dias_ingresado': 10,
    'fechaNacimiento': '1990-05-20',
    'diagnostico': 'Hipertensión'
}

pac = UsuarioFactory.crear(datos)   # genera nombreUsuario automáticamente → 'mariagarcia'

UsuarioDAO.create(pac)              # 1. inserta en Usuarios
PacienteDAO.create(pac)             # 2. inserta en Pacientes
PacPubDAO.create(pac)               # 3. inserta en Pac_pub


# --- Crear un administrador (insert en cascada) ---
from app.dao.nuevos_dao import AdministradorDAO

datos = {
    'Rol': 'admin',
    'Nombre': 'Carlos',
    'apellidos': 'Ruiz Mora',
    'DNI': '99887766Z',
    'password': 'admin123',
    'nombreUsuario': 'admin'        # los admins pueden tener nombreUsuario fijo
}

admin = UsuarioFactory.crear(datos)

UsuarioDAO.create(admin)            # 1. inserta en Usuarios
AdministradorDAO.create(admin)      # 2. inserta en Administrador


# --- Crear una evaluación profesional ---
from app.dao.nuevos_dao import EvaluacionProfesionalDAO
from app.models.nuevos import EvaluacionProfesional

ev = EvaluacionProfesional(
    Paciente='mariagarcia',
    Trabajador='pedromendes',
    fecha='2024-03-15',
    movilidad='buena',
    estadoEmocional='estable',
    apetito='normal',
    observaciones='Evolución positiva'
)

id_ev = EvaluacionProfesionalDAO.create(ev)


# --- Crear una factura ---
from app.dao.nuevos_dao import FacturaDAO
from app.models.nuevos import Factura

factura = Factura(
    codigoFactura='FAC-2024-001',
    Paciente='mariagarcia',
    Administrador='admin',
    fechaEmision='2024-03-31',
    importeTotal=450.00,
    estadoPago='pendiente'
)

FacturaDAO.create(factura)
FacturaDAO.update_estado('FAC-2024-001', 'pagado')


# --- Borrar un usuario (borrado lógico) ---
UsuarioDAO.delete('mariagarcia')    # marca activo = 0, no elimina el registro
```

---

## 🛡️ REGLAS DE ORO

- **NUNCA** concatenes strings en SQL — usa siempre parámetros: `cursor.execute(sql, (val1, val2))`
- **SIEMPRE** cierra el cursor en `finally`
- **NUNCA** cierres la conexión — la gestiona el Singleton
- Usa `conn.rollback()` si hay error en INSERT / UPDATE / DELETE
- Los inserts son **siempre en cascada** — el orden importa:
  - Paciente: `Usuarios` → `Pacientes` → `Pac_pub`/`Pac_pri`
  - Trabajador: `Usuarios` → `Trabajadores` → `Auxiliares`/`coordinadores`/`Especialistas`
  - Admin: `Usuarios` → `Administrador`
- Esa cascada la gestiona el **controlador**, no el DAO
- El borrado de usuarios es **lógico** (`activo = 0`) — nunca se elimina el registro

---

## 📝 CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR
- `create` de `PacienteDAO` ahora incluye `fechaNacimiento`, `foto` y `diagnostico` 
- Añadidos `EvaluacionProfesionalDAO`, `InformeDAO` y `FacturaDAO` en `eval_inf_fac_dao.py`