from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required

# Definimos el blueprint con prefijo y carpeta de plantillas
paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente', template_folder='templates/paciente')

# Tu Panel Principal
@paciente_bp.route('/dashboard')
@login_required
@role_required('paciente')
def dashboard():
    return render_template('paciente/dashboard.html')

# CU-07: Mostrar el cuestionario
@paciente_bp.route('/cuestionario')
@login_required
@role_required('paciente')
def cuestionario():
    return render_template('paciente/cuestionario.html')

# CU-08: Guardar lo que responda el paciente
@paciente_bp.route('/responder', methods=['POST'])
@login_required
@role_required('paciente')
def responder():
    flash("¡Cuestionario guardado con éxito!", "success")
    return redirect(url_for('paciente.dashboard'))

# CU-02: Ver perfil propio (AÑADIDO PARA SOLUCIONAR EL ERROR)
@paciente_bp.route('/perfil')
@login_required
@role_required('paciente')
def perfil():
    return render_template('paciente/perfil.html')