from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required
from app.dao.usuario_dao import UsuarioDAO
from app.dao.paciente_dao import PacienteDAO

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')

@paciente_bp.route('/dashboard')
@login_required
@role_required('paciente')
def dashboard():
    return render_template('paciente/dashboard.html')

@paciente_bp.route('/cuestionario')
@login_required
@role_required('paciente')
def cuestionario():
    return render_template('paciente/cuestionario.html')

@paciente_bp.route('/responder', methods=['POST'])
@login_required
@role_required('paciente')
def responder():
    flash("¡Cuestionario guardado con éxito!", "success")
    return redirect(url_for('paciente.dashboard'))

@paciente_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@role_required('paciente')
def perfil():
    if request.method == 'POST':
        flash("Cambios guardados correctamente.", "success")
        return redirect(url_for('paciente.perfil'))

    username = session.get('usuario')

    usuario_db = UsuarioDAO.get_by_nombreUsuario(username)
    paciente_db = PacienteDAO.get_by_nombreUsuario(username)

    return render_template('paciente/perfil.html', usuario=usuario_db, paciente=paciente_db)