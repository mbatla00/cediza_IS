from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .auth import login_required, role_required
from src.modelo.dao import UsuarioDAO, PacienteDAO, FamiliarDAO, CuestionarioDAO, PreguntaDAO, RespuestaDAO
from src.modelo.vo import Respuesta
from datetime import datetime, date

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')


# --- PANEL PRINCIPAL DEL PACIENTE ---
@paciente_bp.route('/dashboard')
@login_required
@role_required('paciente')
def dashboard():
    username = session.get('usuario')

    # Comprobamos si el paciente ya respondió el cuestionario hoy
    respuestas_hoy = RespuestaDAO.get_by_paciente(username)
    ya_respondio_hoy = any(
        r.fechaHora and r.fechaHora.date() == date.today()
        for r in respuestas_hoy
    )

    return render_template('paciente/dashboard.html',
                           ya_respondio_hoy=ya_respondio_hoy)


# --- CU-07: MOSTRAR CUESTIONARIO DIARIO ---
@paciente_bp.route('/cuestionario')
@login_required
@role_required('paciente')
def cuestionario():
    username = session.get('usuario')

    # Bloquear si ya respondió hoy
    respuestas_hoy = RespuestaDAO.get_by_paciente(username)
    ya_respondio_hoy = any(
        r.fechaHora and r.fechaHora.date() == date.today()
        for r in respuestas_hoy
    )
    if ya_respondio_hoy:
        flash('Ya has completado el cuestionario de hoy. ¡Hasta mañana!', 'info')
        return redirect(url_for('paciente.dashboard'))

    # Cargamos el cuestionario diario
    cuestionarios = CuestionarioDAO.get_all()
    cuestionario_diario = next(
        (c for c in cuestionarios if c.tipo == 'diario'), None
    )

    if not cuestionario_diario:
        flash('No hay cuestionario disponible para hoy.', 'info')
        return redirect(url_for('paciente.dashboard'))

    preguntas = PreguntaDAO.get_by_cuestionario(cuestionario_diario.idCuestionario)

    if not preguntas:
        flash('El cuestionario no tiene preguntas configuradas.', 'warning')
        return redirect(url_for('paciente.dashboard'))

    return render_template('paciente/cuestionario.html',
                           cuestionario=cuestionario_diario,
                           preguntas=preguntas)


# --- CU-08: GUARDAR RESPUESTAS DEL CUESTIONARIO ---
@paciente_bp.route('/responder', methods=['POST'])
@login_required
@role_required('paciente')
def responder():
    username = session.get('usuario')
    ahora = datetime.now()

    errores = False
    for key, valor in request.form.items():
        if key.startswith('respuesta_'):
            try:
                id_pregunta = int(key.replace('respuesta_', ''))
            except ValueError:
                continue

            contenido = valor.strip()
            if not contenido:
                continue

            nueva_respuesta = Respuesta(
                idPregunta=id_pregunta,
                idPaciente=username,
                fechaHora=ahora,
                contenido=contenido
            )

            if not RespuestaDAO.create(nueva_respuesta):
                errores = True

    if errores:
        flash('Hubo un error al guardar algunas respuestas. Inténtalo de nuevo.', 'danger')
    else:
        flash('¡Cuestionario enviado con éxito! Gracias.', 'success')

    return redirect(url_for('paciente.dashboard'))


# --- CU-02: VER Y ACTUALIZAR PERFIL DEL PACIENTE ---
@paciente_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@role_required('paciente')
def perfil():
    username = session.get('usuario')

    if request.method == 'POST':
        nuevo_email = request.form.get('email', '').strip()

        usuario_db = UsuarioDAO.get_by_nombreUsuario(username)
        if not usuario_db:
            flash('Error: usuario no encontrado.', 'danger')
            return redirect(url_for('paciente.perfil'))

        usuario_db.email = nuevo_email if nuevo_email else None

        if UsuarioDAO.update(usuario_db):
            flash('Cambios guardados correctamente.', 'success')
        else:
            flash('Error al guardar los cambios. Inténtalo de nuevo.', 'danger')

        return redirect(url_for('paciente.perfil'))

    # GET: cargar datos desde BD
    usuario_db = UsuarioDAO.get_by_nombreUsuario(username)
    paciente_db = PacienteDAO.get_by_nombreUsuario(username)
    familiares = FamiliarDAO.get_by_paciente(username)

    return render_template('paciente/perfil.html',
                           usuario=usuario_db,
                           paciente=paciente_db,
                           familiares=familiares)




# --- VER HISTORIAL MÉDICO DEL PACIENTE ---
@paciente_bp.route('/historial')
@login_required
@role_required('paciente')
def historial():
    """Muestra el historial de respuestas del paciente"""
    username = session.get('usuario')
    
    # Obtener todas las respuestas del paciente
    respuestas = RespuestaDAO.get_by_paciente(username)
    
    # Agrupar respuestas por fecha (como espera el template)
    historial_agrupado = {}
    for respuesta in respuestas:
        if respuesta.fechaHora:
            fecha = respuesta.fechaHora.date()
            if fecha not in historial_agrupado:
                historial_agrupado[fecha] = []
            historial_agrupado[fecha].append(respuesta)
    
    # Obtener diccionario de preguntas para mostrar el texto de la pregunta
    preguntas_dict = {}
    todas_las_preguntas = PreguntaDAO.get_all()  # Necesitas este método
    for pregunta in todas_las_preguntas:
        preguntas_dict[pregunta.idPregunta] = pregunta.texto
    
    return render_template('paciente/historial.html',
                          historial_agrupado=historial_agrupado,
                          preguntas_dict=preguntas_dict)