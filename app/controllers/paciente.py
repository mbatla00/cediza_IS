from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required
from app.dao.usuario_dao import UsuarioDAO
from app.dao.paciente_dao import PacienteDAO

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')


# --- PANEL PRINCIPAL DEL PACIENTE ---
@paciente_bp.route('/dashboard')
@login_required
@role_required('paciente')
def dashboard():
    return render_template('paciente/dashboard.html')


# --- CU-07: MOSTRAR CUESTIONARIO DIARIO ---
@paciente_bp.route('/cuestionario')
@login_required
@role_required('paciente')
def cuestionario():
    return render_template('paciente/cuestionario.html')


# --- CU-08: GUARDAR RESPUESTAS DEL CUESTIONARIO ---
@paciente_bp.route('/responder', methods=['POST'])
@login_required
@role_required('paciente')
def responder():
    # TODO: cuando Sofía cree los DAOs de cuestionarios,
    # aquí se recogerán los datos del formulario
    # y se insertarán en BD usando RespuestaDAO.create(...)
    flash('¡Cuestionario guardado con éxito!', 'success')
    return redirect(url_for('paciente.dashboard'))


# --- CU-02: VER Y ACTUALIZAR PERFIL DEL PACIENTE ---
@paciente_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@role_required('paciente')
def perfil():
    username = session.get('usuario')

    if request.method == 'POST':
        nuevo_email = request.form.get('email', '').strip()
        password_actual = request.form.get('password_actual', '').strip()
        password_nueva = request.form.get('password_nueva', '').strip()
        password_repetir = request.form.get('password_repetir', '').strip()

        usuario_db = UsuarioDAO.get_by_nombreUsuario(username)
        if not usuario_db:
            flash('Error: usuario no encontrado.', 'danger')
            return redirect(url_for('paciente.perfil'))

        # Actualizar email
        usuario_db.email = nuevo_email if nuevo_email else None

        # Cambio de contraseña (solo si se ha rellenado algún campo)
        if password_actual or password_nueva or password_repetir:
            if usuario_db.password != password_actual:
                flash('La contraseña actual no es correcta.', 'danger')
                return redirect(url_for('paciente.perfil'))
            if password_nueva != password_repetir:
                flash('Las contraseñas nuevas no coinciden.', 'danger')
                return redirect(url_for('paciente.perfil'))
            if not password_nueva:
                flash('La nueva contraseña no puede estar vacía.', 'danger')
                return redirect(url_for('paciente.perfil'))
            usuario_db.password = password_nueva

        if UsuarioDAO.update(usuario_db):
            flash('Cambios guardados correctamente.', 'success')
        else:
            flash('Error al guardar los cambios. Inténtalo de nuevo.', 'danger')

        return redirect(url_for('paciente.perfil'))

    # GET: cargar datos desde BD
    usuario_db = UsuarioDAO.get_by_nombreUsuario(username)
    paciente_db = PacienteDAO.get_by_nombreUsuario(username)

    return render_template('paciente/perfil.html', usuario=usuario_db, paciente=paciente_db)