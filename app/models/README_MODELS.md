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
├── usuario.py          → Usuario (clase base)
├── paciente.py         → Paciente (hereda de Usuario)
├── paciente_tipos.py   → PacientePublico, PacientePrivado (heredan de Paciente)
├── trabajador.py       → Trabajador (hereda de Usuario)
├── trabajador_tipos.py → Auxiliar, Coordinador, Especialista (heredan de Trabajador)
└── familiar.py         → Atributo multivalorado de paciente 
└──comentario.py        → Tiene auxiliar(FK), paciente(FK), dia y nota(mensaje)   
└──sesion.py            → Tiene especialista(FK), paciente(FK), fecha y nota(mensaje)
```

## 🔗 JERARQUÍA DE HERENCIA

```
Usuario
├── Paciente
│   ├── PacientePublico   (Dias_ingresado en hospital — para facturación)
│   └── PacientePrivado   (IVA, cuenta, horas)
└── Trabajador
    ├── Auxiliar          (Horario)
    ├── Coordinador       (infoInteres)
    └── Especialista      (Especialidad, Horario)
```

**Nunca instancies `Usuario`, `Paciente` o `Trabajador` directamente.**
Usa siempre la factoría (`factories/usuario_factory.py`) para crear objetos,
o el subtipo concreto si sabes exactamente lo que estás creando.

---

## 📝 REGLAS DE ORO

- **Todos los atributos son privados** (con `_`) y se accede a ellos mediante `@property`
- **`to_dict()`** es obligatorio en cada clase — convierte el objeto a diccionario para enviarlo a las vistas
- **Nada de SQL aquí** — si necesitas ir a la BD, estás en el sitio equivocado
- Los setters de `fecha`/`dia` aceptan tanto `str` `'YYYY-MM-DD'` como objeto `date` — internamente siempre guardan un `date`
- El setter de `telefono` en `Familiar` solo acepta exactamente 9 dígitos

---

## 💡 EJEMPLO DE USO

```python
# Crear un objeto directamente (si ya sabes el tipo)
from app.models.paciente_tipos import PacientePublico

pac = PacientePublico(
    nombreUsuario='GarciaLopezMaria',
    Nombre='Maria Garcia Lopez',
    DNI='12345678A',
    contraseña='1234',
    Dias_ingresado=12
)

print(pac.nombre)       # 'Maria Garcia Lopez'
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
- Si no se inserta nombreUsuario al crear un `Usuario` se le pondrá por defecto 'ApellidoNombre'. OJO‼️si hay dos nombreUsuario iguales el controlador debera añadir un nº al crear al nuevo usuario