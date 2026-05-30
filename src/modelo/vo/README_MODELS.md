# 📦 GUÍA PARA MODELOS (Value Objects - VO)

## ¿Qué es esta carpeta?
Aquí van las clases que representan las **tablas de la base de datos**.
Son clases simples: solo atributos, getters, setters y `to_dict()`.
**No incluyen ninguna lógica de base de datos** — eso va en `dao/`.

## Responsable: Sofía

---

## 🗂️ ARCHIVOS Y CLASES

```
models/
├── usuarioVO.py          → Usuario (clase base)
├── pacienteVO.py         → Paciente (hereda de Usuario)
├── pacPriVO.py           → Paciente privado (hereda de paciente)
├── pacPubVO.py           → Paciente publico (hereda de paciente)
├── trabajadorVO.py       → Trabajador (hereda de Usuario)
├── auxiliarVO.py         → Auxiliar (hereda de trabajador)
├── coordinadorVO.py      → Coordinador (hereda de trabajador)
├── especialistaVO.py     → Especialista (hereda de trabajador)
├── familiarVO.py         → Atributo multivalorado de paciente
├── comentarioVO.py       → Comentario de un auxiliar a un paciente
├── sesionVO.py           → Sesion de un especialista con un paciente
├── cuestionarioVO.py     → Cuestionario para los pacientes
├── preguntaVO.py         → Preguntas de los cuestionarios
├── respuestaVO.py        → Respuesta de un paciente a una pregunta
├── evaluacionVO.py       → Evaluacion de un trabajador a un paciente
├── informeVO.py          → Informe de un trabajador sobre un paciente
├── facturaVO.py          → Factura de un paciente en una fecha
└──adminVO.py             → Administrador (hereda de usuario)
```

## 🔗 JERARQUÍA DE HERENCIA

```
Usuario
├── Paciente
│   ├── PacientePublico   (Dias_ingresado en hospital — para facturación)
│   └── PacientePrivado   (IVA, cuenta, horas)
├── Trabajador
│   ├── Auxiliar          (Horario)
│   ├── Coordinador       (infoInteres)
│   └── Especialista      (Especialidad, Horario)
└── Administrador         (gestiona facturas)
```

**Nunca instancies `Usuario`, `Paciente` o `Trabajador` directamente.**
Usa siempre la factoría (`factories/usuario_factory.py`) para crear objetos,
o el subtipo concreto si sabes exactamente lo que estás creando.

---

## 📝 REGLAS DE ORO

- **Todos los atributos son privados** (con `_`) y se accede a ellos mediante `@property`
- **`to_dict()`** es obligatorio en cada clase — convierte el objeto a diccionario para enviarlo a las vistas
- **Nada de SQL aquí** — si necesitas ir a la BD, estás en el sitio equivocado
- Los setters de `fecha`/`dia`/`fechaHora` aceptan tanto `str` como objeto `date`/`datetime` — internamente siempre guardan el tipo correcto
- El setter de `telefono` en `Familiar` solo acepta exactamente 9 dígitos
- `foto` en `Paciente` es un `VARCHAR` con la ruta a la imagen, no la imagen en binario

---

## 💡 EJEMPLO DE USO

```python
# Crear un objeto directamente (si ya sabes el tipo)
from app.models.paciente_tipos import PacientePublico

pac = PacientePublico(
    nombreUsuario='mariagarcia',
    Nombre='Maria Garcia Lopez',
    DNI='12345678A',
    password='1234',
    Dias_ingresado=12,
    fechaNacimiento='1990-05-20',
    diagnostico='Hipertensión'
)

print(pac.nombre)       # 'Maria'
print(pac.tipo)         # 'publico'
print(pac.to_dict())    # {'nombreUsuario': ..., 'nombre': ..., 'tipo': 'publico', ...}

# Modificar un atributo
pac.dias_ingresado = 15

# Lo más habitual: crear desde un dict (datos de un formulario o de la BD)
# Para eso usa la factoría → ver factories/README.md
```

---

## ⚠️ IMPORTANTE

- `PacientePublico` y `PacientePrivado` son los nombres completos — en la BD las tablas
  se llaman `Pac_pub` y `Pac_pri` pero en el código usamos nombres legibles
- `dias_ingresado` en `PacientePublico` representa los días del mes que el paciente
  ha estado ingresado en un **hospital externo**, dato necesario para la facturación
- El campo `Auxiliar` en `Comentario` es una FK a `Trabajadores` — aunque el nombre
  diga "Auxiliar", cualquier tipo de trabajador puede escribir comentarios
- `Administrador` hereda de `Usuario` y gestiona las facturas de los pacientes
- `EvaluacionProfesional` e `Informe` los crea cualquier trabajador, no solo especialistas
