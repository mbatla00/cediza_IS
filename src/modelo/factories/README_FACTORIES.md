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
├── TrabajadorFactory   ← lee el campo 'Tipo' → Auxiliar | Coordinador | Especialista
└── Admin               ← rol 'admin', se crea directamente sin subfactoría
```

Normalmente solo usarás `UsuarioFactory.crear(datos)` — las subfactorías
las llama ella internamente.

---

## 🔑 GENERACIÓN AUTOMÁTICA DE NOMBRE DE USUARIO

Si el dict de datos **no incluye** `nombreUsuario`, la factoría lo genera
automáticamente a partir del campo `Nombre` con el formato `NombreApellido1` en minúsculas:

| Nombre completo | nombreUsuario generado |
|---|---|
| `'Maria Garcia Lopez'` | `'mariagarcia'` |
| `'Maria Carmen Garcia Lopez'` | `'mariagarcia'` (sin sufijo — lo gestiona el controlador) |

El formato asume:
- **3 partes** → `'Nombre Apellido1 Apellido2'` → usa `Nombre + Apellido1`
- **4 partes** → `'Nombre1 Nombre2 Apellido1 Apellido2'` → usa `Nombre1 + Apellido1`

> ⚠️ Si el `nombreUsuario` ya existe en BD, el método `generar_nombre_usuario`
> en `UsuarioDAO` añade automáticamente un sufijo numérico
> (`'mariagarcia1'`, `'mariagarcia2'`...) hasta encontrar uno libre.

---

## 💡 EJEMPLO DE USO

```python
from app.factories.usuario_factory import UsuarioFactory

# --- Caso 1: paciente desde formulario ---
datos_formulario = {
    'Rol': 'paciente',
    'Tipo': 'privado',
    'Nombre': 'Carlos Ruiz Mora',
    'DNI': '87654321B',
    'password': 'pass123',
    'IVA': 21,
    'cuenta': 'ES12 1234 5678 9012 3456 7890',
    'horas': 10,
    'fechaNacimiento': '1985-03-10',
    'diagnostico': 'Ansiedad'
}

paciente = UsuarioFactory.crear(datos_formulario)
# nombreUsuario se genera automáticamente → 'carlosruiz'
# devuelve un objeto PacientePrivado


# --- Caso 2: trabajador desde la BD (row de un JOIN) ---
row = {
    'Rol': 'trabajador',
    'Tipo': 'especialista',
    'nombreUsuario': 'lauramartinez',
    'Nombre': 'Laura Martinez Gil',
    'DNI': '11223344C',
    'password': 'pass456',
    'Especialidad': 'Psicología',
    'Horario': 'Mañanas'
}

especialista = UsuarioFactory.crear(row)
# nombreUsuario ya viene en el dict → no se genera
# devuelve un objeto Especialista
print(especialista.especialidad)    # 'Psicología'
print(especialista.tipo)            # 'especialista'


# --- Caso 3: administrador ---
datos_admin = {
    'Rol': 'admin',
    'nombreUsuario': 'admin',
    'Nombre': 'Administrador',
    'DNI': '12345678Z',
    'password': 'admin123'
}

admin = UsuarioFactory.crear(datos_admin)
# devuelve un objeto Administrador


# --- Caso 4: usar subfactoría directamente ---
# Solo si ya sabes el tipo concreto y quieres saltarte el paso de Rol
from app.factories.usuario_factory import TrabajadorFactory

trabajador = TrabajadorFactory.crear({
    'Tipo': 'auxiliar',
    'Nombre': 'Juan Lopez Reyes',
    'DNI': '99887766D',
    'password': 'pass789',
    'Horario': 'Tardes'
})
```

---

## ⚠️ ERRORES COMUNES

```python
# ❌ Tipo de paciente desconocido
PacienteFactory.crear({'Tipo': 'vip', ...})
# ValueError: Tipo de paciente desconocido: 'vip'. Valores válidos: 'publico', 'privado'

# ❌ Tipo de trabajador desconocido
TrabajadorFactory.crear({'Tipo': 'becario', ...})
# ValueError: Tipo de trabajador desconocido: 'becario'. Valores válidos: 'auxiliar', 'coordinador', 'especialista'

# ❌ Nombre con formato incorrecto (no genera nombreUsuario)
UsuarioFactory._generar_nombreUsuario('Maria')
# ValueError: El nombre debe tener al menos nombre y un apellido

# ✅ Admin sí es un rol válido
UsuarioFactory.crear({'Rol': 'admin', 'nombreUsuario': 'admin', 'Nombre': 'Administrador', 'DNI': '12345678Z', 'password': 'admin123'})
# Devuelve un objeto Administrador
```

---

## 📝 CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR

- **Añadido rol `admin`**: se crea directamente como objeto `Administrador` sin pasar por subfactoría
- **Formato de `nombreUsuario`**: ahora es `NombreApellido1` en minúsculas (ej: `mariagarcia`)
- **Todas las factorías usan `password`** en lugar de `contraseña` para coincidir con la BD
- **El método `generar_nombre_usuario`** en `UsuarioDAO` ya evita duplicados añadiendo sufijo numérico