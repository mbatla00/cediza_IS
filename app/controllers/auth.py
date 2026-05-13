"""
Controlador de autenticación y seguridad.

Este archivo contiene:
- Login y logout de usuarios
- Conexión a base de datos real mediante UsuarioDAO
- Decoradores de seguridad: @login_required y @role_required
- Redirección al dashboard según el rol del usuario
- Patrón Factory: DashboardFactory decide qué vista mostrar según el rol

Es la columna vertebral de la seguridad del proyecto.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.dao.usuario_dao import UsuarioDAO

# Blueprint que agrupa todas las rutas de autenticación
auth_bp = Blueprint('auth', __name__)


# ============================================================
# PATRÓN FACTORY: Decide qué dashboard mostrar según el rol
# ============================================================
class DashboardFactory:
    """Fábrica que devuelve la plantilla correcta según el rol del usuario"""

    @staticmethod
    def get_template(rol):
        """Devuelve la ruta de la plantilla según el rol"""
        plantillas = {
            'admin': 'admin/dashboard.html',
            'trabajador': 'trabajador/dashboard.html',
            'paciente': 'paciente/dashboard.html',
        }
        return plantillas.get(rol)


# ============================================================
# DECORADORES DE SEGURIDAD
# ============================================================

def login_required(f):
    """
    Decorador que obliga a estar logueado para acceder a una ruta.
    Si el usuario no ha iniciado sesión, le redirige al login.
    Uso: @login_required encima de cualquier ruta que necesite protección.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles_permitidos):
    """
    Decorador que restringe el acceso según el rol del usuario.
    Recibe los roles que tienen permiso (admin, trabajador, paciente).
    Si el usuario no tiene el rol adecuado, le redirige a su dashboard.

    Uso: @role_required('admin')
          @role_required('admin', 'trabajador')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'rol' not in session or session['rol'] not in roles_permitidos:
                flash('No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('auth.dashboard_redirect'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================

@auth_bp.route('/')
def index():
    """Redirige según si hay sesión activa o no"""
    if 'usuario' in session:
        return redirect(url_for('auth.dashboard_redirect'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Pantalla de inicio de sesión.
    GET: muestra el formulario de login.
    POST: valida credenciales contra la base de datos real.
    """
    if request.method == 'POST':
        usuario_input = request.form.get('usuario')
        password = request.form.get('password')

        # Buscar en la base de datos real
        usuario = UsuarioDAO.get_by_nombreUsuario(usuario_input)

        if usuario and usuario.contraseña == password:
            session['usuario_nombre'] = usuario.nombre
            session['usuario'] = usuario_input
            session['rol'] = usuario.rol
            flash(f'¡Bienvenido/a {usuario.nombre}!', 'success')
            return redirect(url_for('auth.dashboard_redirect'))

        # Credenciales incorrectas
        flash('Usuario o contraseña incorrectos', 'danger')

    # GET: mostrar formulario de login
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario y limpia todos los datos"""
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard_redirect():
    """
    Redirige al dashboard correspondiente según el rol.
    Usa el patrón Factory para decidir qué plantilla mostrar.
    """
    rol = session.get('rol')
    template = DashboardFactory.get_template(rol)

    if template:
        return render_template(template)

    flash('Error: rol no reconocido', 'danger')
    return redirect(url_for('auth.login'))