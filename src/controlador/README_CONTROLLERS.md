# 🎮 GUÍA PARA CONTROLADORES

## ¿Qué es esta carpeta?
Aquí se definen las **rutas** de la aplicación Flask. Cada archivo agrupa
rutas relacionadas según el rol del usuario.

## Responsables: María (auth), Mario y Alejandro (resto)

---

## 🔐 DECORADORES DE SEGURIDAD (YA IMPLEMENTADOS)

Todos los controladores deben usar estos decoradores que están en `auth.py`:

```python
from app.controllers.auth import login_required, role_required

# Ejemplo de uso:
@admin_bp.route('/dashboard')
@login_required              # Primero: verifica que está logueado
@role_required('admin')      # Segundo: verifica que tiene el rol correcto
def dashboard():
    return render_template('admin/dashboard.html')
```

## 📝 PLANTILLA PARA UN CONTROLADOR NUEVO

```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required

# Crear el Blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    return render_template('admin/dashboard.html')
```

## 📋 RUTAS PENDIENTES DE IMPLEMENTAR

### Auth (auth.py) - ✅ IMPLEMENTADO
- `/login` - Inicio de sesión contra BD real mediante `UsuarioDAO`
- `/logout` - Cierre de sesión
- `/dashboard` - Redirección según rol (Factory: admin, trabajador, paciente)

### Admin (admin.py)
- `/admin/dashboard` - Panel principal
- `/admin/pacientes/nuevo` - CU-01: Dar de alta paciente (GET y POST)
- `/admin/usuarios` - Listar usuarios
- `/admin/usuarios/<id>/baja` - CU-04: Dar de baja

### Trabajador (trabajador.py)
- `/trabajador/dashboard` - Panel principal
- `/trabajador/pacientes` - Lista de pacientes
- `/trabajador/paciente/<id>/ver` - CU-02: Ver perfil del paciente
- `/trabajador/paciente/<id>/nota` - CU-09: Añadir nota libre
- `/trabajador/paciente/<id>/evaluacion` - CU-10: Evaluación rápida
- `/trabajador/paciente/<id>/historial` - CU-11: Historial unificado

### Paciente (paciente.py)
- `/paciente/dashboard` - Panel principal
- `/paciente/cuestionario` - CU-07: Mostrar preguntas diarias
- `/paciente/responder` - CU-08: Guardar respuestas
- `/paciente/perfil` - CU-02: Ver perfil propio (limitado)

---

## 📝 CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR

- El login ya no usa credenciales fake. Conecta con la BD real mediante `UsuarioDAO.get_by_nombreUsuario`.
- El rol `admin` está completamente soportado y redirige a `admin/dashboard.html`.
- Las credenciales de prueba actuales son:
  - `admin` / `admin123`
  - `anagarcia` / `trab123` (trabajador - auxiliar)
  - `mariagarcia` / `1234` (paciente público)