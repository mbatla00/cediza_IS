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
        nombre_completo = request.form.get('nombre_completo')
        dni = request.form.get('dni')
        email = request.form.get('email')
        fecha_nacimiento_input = request.form.get('fecha_nacimiento') # <--- CAPTURAMOS EL NUEVO CAMPO
        tipo = request.form.get('tipo')
        cuenta = request.form.get('cuenta')
        nombre_usuario_manual = request.form.get('nombre_usuario_manual')

        # Controlamos si la fecha viene vacía del HTML para transformarla en NULL seguro
        fecha_nacimiento = fecha_nacimiento_input if fecha_nacimiento_input and fecha_nacimiento_input.strip() else None

        # LÓGICA DE DECISIÓN DEL NOMBRE DE USUARIO
        if nombre_usuario_manual and nombre_usuario_manual.strip():
            nombre_usuario = nombre_usuario_manual.strip().replace(' ', '').lower()[:50]
        else:
            nombre_usuario = nombre_completo.replace(' ', '').lower()[:50]

        try:
            # CONTROL DE DUPLICADOS
            if UsuarioDAO.get_by_nombreUsuario(nombre_usuario):
                flash(f'El nombre de usuario "{nombre_usuario}" ya está ocupado. Elige otro.', 'warning')
                return redirect(url_for('admin.nuevo_paciente'))

            # A. CREAR EL USUARIO PADRE (Añadimos fechaNacimiento)
            nuevo_usuario = Usuario(
                nombreUsuario=nombre_usuario, 
                Nombre=nombre_completo,
                DNI=dni,
                Rol='paciente',
                password=dni, 
                email=email,
                fechaNacimiento=fecha_nacimiento # <--- SE LO PASAMOS AL MODELO
            )
            
            if not UsuarioDAO.create(nuevo_usuario):
                flash('Error al crear la cuenta de usuario base.', 'danger')
                return redirect(url_for('admin.nuevo_paciente'))

            # B. TABLAS PACIENTES Y TIPO DETALLADO 
            # (Nota: Las tablas específicas no guardan la fecha, solo la tabla padre 'Usuarios')
            if tipo == 'publico':
                nuevo_p = PacPub(
                    nombreUsuario=nombre_usuario, 
                    Nombre=nombre_completo, 
                    DNI=dni,
                    password=dni,
                    Dias_ingresado=0,
                    email=email
                )
                exito = PacienteDAO.create(nuevo_p) and PacPubDAO.create(nuevo_p)
            else:
                if not cuenta:
                    flash('Error: Los pacientes privados necesitan una cuenta bancaria.', 'warning')
                    return redirect(url_for('admin.nuevo_paciente'))
                
                nuevo_p = PacPri(
                    nombreUsuario=nombre_usuario, 
                    Nombre=nombre_completo, 
                    DNI=dni,
                    password=dni,
                    cuenta=cuenta,
                    email=email
                )
                exito = PacienteDAO.create(nuevo_p) and PacPriDAO.create(nuevo_p)

            if exito:
                flash(f'Éxito: Paciente {nombre_completo} ({nombre_usuario}) registrado correctamente.', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Error al guardar datos específicos del paciente.', 'danger')
        
        except Exception as e:
            flash(f'Error crítico de Base de Datos: {str(e)}', 'danger')

    return render_template('admin/paciente_form.html')

# --- CU-04: LISTADO DE USUARIOS (GESTIÓN DE BAJAS) ---
@admin_bp.route('/admin/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    """Muestra la lista de todos los usuarios para poder gestionarlos."""
    try:
        # 1. Llamamos a tu nuevo método del DAO para traer los 5 usuarios de la BD
        usuarios_bd = UsuarioDAO.get_all()
    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        usuarios_bd = []
        flash('Error al cargar la lista de usuarios.', 'danger')
        

    return render_template('admin/usuarios_lista.html', usuarios=usuarios_bd)


# --- CU-05: GESTIÓN DE BAJAS (PACIENTES Y TRABAJADORES) ---
@admin_bp.route('/admin/usuarios/gestion-bajas')
@login_required
@role_required('admin')
def gestion_bajas():
    """Muestra la lista de todos los usuarios usando el DAO original."""
    usuarios_bd = UsuarioDAO.get_all()
    return render_template('admin/usuarios_lista.html', usuarios=usuarios_bd)


@admin_bp.route('/admin/usuarios/cambiar-estado/<nombre_usuario>', methods=['POST'])
@login_required
@role_required('admin')
def cambiar_estado_usuario(nombre_usuario):
    """Procesa el cambio de estado usando los métodos del DAO."""
    estado_actual = request.form.get('estado_actual') == '1' # En MySQL BOOLEAN es 1 o 0
    
    if estado_actual:
        # SI ESTÁ ACTIVO -> Usamos tu método delete() existente para pasarlo a 0
        exito = UsuarioDAO.delete(nombre_usuario)
        accion = "dado de BAJA"
    else:
        # SI ESTÁ INACTIVO -> Lo reactivamos con un query rápido pasándolo a 1
        db = Database()
        conn = db.get_connection()
        exito = False
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE Usuarios SET activo = 1 WHERE nombreUsuario = %s", (nombre_usuario,))
                conn.commit()
                exito = True
            except Exception as e:
                print(f"Error al reactivar: {e}")
            finally:
                cursor.close()
        accion = "REACTIVADO"
    
    if exito:
        flash(f'El usuario {nombre_usuario} ha sido {accion} correctamente.', 'success')
    else:
        flash(f'Error al procesar la solicitud del usuario {nombre_usuario}.', 'danger')
        
    return redirect(url_for('admin.gestion_bajas'))