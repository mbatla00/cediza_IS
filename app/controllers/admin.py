from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required
from app.dao.paciente_dao import PacienteDAO, PacPubDAO, PacPriDAO
from app.models.paciente_tipos import PacPub, PacPri
from app.dao.usuario_dao import UsuarioDAO 
from app.models.usuario import Usuario

# DEFINIMOS EL BLUEPRINT UNA SOLA VEZ
admin_bp = Blueprint('admin', __name__)

# --- CU-00: PANEL PRINCIPAL ---
@admin_bp.route('/admin/dashboard')
@login_required
@role_required('admin')
def dashboard():
    """Muestra el panel principal con acceso a todas las funciones de gestión."""
    return render_template('admin/dashboard.html')

# --- CU-01: ALTA DE PACIENTE ---
@admin_bp.route('/admin/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def nuevo_paciente():
    if request.method == 'POST':
        # 1. Recogemos solo lo que pide la BD
        nombre_completo = request.form.get('nombre_completo')
        dni = request.form.get('dni')
        email = request.form.get('email')
        tipo = request.form.get('tipo')
        cuenta = request.form.get('cuenta')
        
        # 2. Generamos el nombreUsuario quitando espacios y en minúsculas (ej: "juanperezgomez")
        nombre_usuario = nombre_completo.replace(' ', '').lower()[:50]

        try:
            # A. CREAR EL USUARIO PADRE
            nuevo_usuario = Usuario(
                nombreUsuario=nombre_usuario, 
                Nombre=nombre_completo, # Usamos Nombre con mayúscula para que coincida con el init
                DNI=dni,
                Rol='paciente',
                contraseña=dni, 
                email=email
            )

            if not UsuarioDAO.create(nuevo_usuario):
                flash('Error al crear la cuenta de usuario base.', 'danger')
                return redirect(url_for('admin.nuevo_paciente'))
            
            # Guardamos el usuario (Necesario antes que el paciente)
            UsuarioDAO.create(nuevo_usuario)

            # B. TABLAS PACIENTES Y TIPO (Las tablas hijas)
            if tipo == 'publico':
                # Quitamos 'Tipo=tipo' porque el modelo PacPub ya lo pone solo como 'publico'
                nuevo_p = PacPub(
                    nombreUsuario=nombre_usuario, 
                    Nombre=nombre_completo, 
                    DNI=dni,
                    contraseña=dni,
                    Dias_ingresado=0
                )
                exito = PacienteDAO.create(nuevo_p) and PacPubDAO.create(nuevo_p)
            else:
                if not cuenta:
                    flash('Error: Los pacientes privados necesitan una cuenta bancaria.', 'warning')
                    return redirect(url_for('admin.nuevo_paciente'))
                
                # Quitamos 'Tipo=tipo' porque el modelo PacPri ya lo pone solo como 'privado'
                nuevo_p = PacPri(
                    nombreUsuario=nombre_usuario, 
                    Nombre=nombre_completo, 
                    DNI=dni,
                    contraseña=dni,
                    cuenta=cuenta
                )
                exito = PacienteDAO.create(nuevo_p) and PacPriDAO.create(nuevo_p)

            if exito:
                flash(f'Éxito: Paciente {nombre_completo} registrado correctamente.', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Error al guardar datos específicos del paciente.', 'danger')
        
        except Exception as e:
            flash(f'Error crítico de Base de Datos: {str(e)}', 'danger')

    return render_template('admin/paciente_form.html')
# --- CU-04: LISTADO DE USUARIOS ---
@admin_bp.route('/admin/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    return render_template('admin/usuarios_lista.html')