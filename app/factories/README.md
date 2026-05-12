# 🏭 GUÍA PARA FACTORÍAS

## ¿Qué es esta carpeta?
Aquí va la lógica de **creación de objetos**. El patrón Factoría centraliza
cómo se instancian los VOs para que el resto del código no tenga que saber
qué subtipo concreto crear — solo le pasas un diccionario de datos y la
factoría devuelve el objeto correcto.

## Responsable: Sofía

---

## 🗂️ ARCHIVOS Y CLASES

```
factories/
└── usuario_factory.py → UsuarioFactory, PacienteFactory, TrabajadorFactory
```

---

## 🔗 JERARQUÍA DE FACTORÍAS

```
UsuarioFactory          ← entrada principal, lee el campo 'Rol'
├── PacienteFactory     ← lee el campo 'Tipo' → PacientePublico | PacientePrivado
└── TrabajadorFactory   ← lee el campo 'Tipo' → Auxiliar | Coordinador | Especialista
```

Normalmente solo usarás `UsuarioFactory.crear(datos)` — las subfactorías
las llama ella internamente.

---

## 🔑 GENERACIÓN AUTOMÁTICA DE NOMBRE DE USUARIO

Si el dict de datos **no incluye** `nombreUsuario`, la factoría lo genera
automáticamente a partir del campo `Nombre` con el formato `Apellido1Nombre1`:

| Nombre completo | nombreUsuario generado |
|---|---|
| `'Maria Garcia Lopez'` | `'GarciaMaria'` |
| `'Maria Carmen Garcia Lopez'` | `'GarciaMaría'` |

El formato asume:
- **3 partes** → `'Nombre Apellido1 Apellido2'`
- **4 partes** → `'Nombre1 Nombre2 Apellido1 Apellido2'`

> ⚠️ Pueden generarse `nombreUsuario` duplicados. El controlador debe
> comprobar si ya existe en BD antes de insertar y añadir un sufijo numérico
> si colisiona (`'GarciaMaria2'`, `'GarciaMaria3'`...).

---

## 💡 EJEMPLO DE USO

```python
from app.factories.usuario_factory import UsuarioFactory

# --- Caso 1: datos vienen de un formulario ---
datos_formulario = {
    'Rol': 'paciente',
    'Tipo': 'privado',
    'Nombre': 'Carlos Ruiz Mora',
    'DNI': '87654321B',
    'contraseña': 'pass123',
    'IVA': 21,
    'cuenta': 'ES12 1234 5678 9012 3456 7890',
    'horas': 10
}

paciente = UsuarioFactory.crear(datos_formulario)
# nombreUsuario se genera automáticamente → 'RuizCarlos'
# devuelve un objeto PacientePrivado


# --- Caso 2: datos vienen de la BD (row de un JOIN) ---
row = {
    'Rol': 'trabajador',
    'Tipo': 'especialista',
    'nombreUsuario': 'MartinezLaura',
    'Nombre': 'Laura Martinez Gil',
    'DNI': '11223344C',
    'contraseña': 'pass456',
    'Especialidad': 'Psicología',
    'Horario': 'Mañanas'
}

especialista = UsuarioFactory.crear(row)
# nombreUsuario ya viene en el dict → no se genera
# devuelve un objeto Especialista
print(especialista.especialidad)    # 'Psicología'
print(especialista.tipo)            # 'especialista'


# --- Caso 3: usar subfactoría directamente ---
# Solo si ya sabes que es un trabajador y quieres saltarte el paso de Rol
from app.factories.usuario_factory import TrabajadorFactory

trabajador = TrabajadorFactory.crear({
    'Tipo': 'auxiliar',
    'Nombre': 'Juan Lopez Reyes',
    'DNI': '99887766D',
    'contraseña': 'pass789',
    'Horario': 'Tardes'
})
```

---

## ⚠️ ERRORES COMUNES

```python
# ❌ Rol desconocido
UsuarioFactory.crear({'Rol': 'admin', ...})
# ValueError: Rol desconocido: 'admin'. Valores válidos: 'paciente', 'trabajador'

# ❌ Tipo desconocido
PacienteFactory.crear({'Tipo': 'vip', ...})
# ValueError: Tipo de paciente desconocido: 'vip'. Valores válidos: 'publico', 'privado'

# ❌ Nombre con formato incorrecto (no genera nombreUsuario)
UsuarioFactory._generar_nombreUsuario('Maria')
# ValueError: El nombre debe tener al menos nombre y un apellido
```