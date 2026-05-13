from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Importamos los decoradores de seguridad desde el archivo de María
from app.controllers.auth import login_required, role_required

# Definimos el Blueprint para el administrador
admin_bp = Blueprint('admin', __name__)

# --- CU-00: PANEL PRINCIPAL ---
@admin_bp.route('/admin/dashboard')
@login_required              # Verifica que 'usuario' esté en la sesión
@role_required('admin')      # Verifica que session['rol'] == 'admin'
def dashboard():
    """Muestra el panel principal con acceso a todas las funciones de gestión."""
    # Renderizamos la plantilla usando la herencia de base.html
    return render_template('admin/dashboard.html')

# --- CU-01: ALTA DE PACIENTE ---
@admin_bp.route('/admin/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def nuevo_paciente():
    """Gestión de alta de nuevos pacientes en el sistema."""
    if request.method == 'POST':
        # Aquí recogeremos los datos con request.form.get()
        # Por ahora, simulamos el éxito y usamos flash para avisar al usuario
        flash('Paciente dado de alta correctamente', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/paciente_form.html')

# --- CU-04: LISTADO Y BAJA DE USUARIOS ---
@admin_bp.route('/admin/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    """Muestra la lista de trabajadores y pacientes para su gestión."""
    return render_template('admin/usuarios_lista.html')