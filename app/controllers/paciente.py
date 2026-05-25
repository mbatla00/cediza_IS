from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required
from app.dao.usuario_dao import UsuarioDAO
from app.dao.paciente_dao import PacienteDAO
from app.dao.otros_dao import FamiliarDAO
from app.dao.cuestionario_dao import CuestionarioDAO, PreguntaDAO, RespuestaDAO
from app.models.cuestionario import Respuesta
from app.dao.database import Database
from datetime import datetime, date

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')


# --- PANEL PRINCIPAL DEL PACIENTE ---
@paciente_bp.route('/dashboard')
@login_required
@role_required('paciente')
def dashboard():
    username = session.get('usuario')

    respuestas_hoy = RespuestaDAO.get_by_paciente(username)
    ya_respondio_hoy = any(
        r.fechaHora and r.fechaHora.date() == date.today()
        for r in respuestas_hoy
    )

    return render_template('paciente/dashboard.html',
                           ya_respondio_hoy=ya_respondio_hoy)


# --- MOSTRAR CUESTIONARIO DIARIO ---
@paciente_bp.route('/cuestionario')
@login_required
@role_required('paciente')
def cuestionario():
    username = session.get('usuario')

    respuestas_hoy = RespuestaDAO.get_by_paciente(username)
    ya_respondio_hoy = any(
        r.fechaHora and r.fechaHora.date() == date.today()
        for r in respuestas_hoy
    )
    if ya_respondio_hoy:
        flash('Ya has completado el cuestionario de hoy. ¡Hasta mañana!', 'info')
        return redirect(url_for('paciente.dashboard'))

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


# --- GUARDAR RESPUESTAS DEL CUESTIONARIO ---
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


# --- VER PERFIL DEL PACIENTE (SOLO LECTURA) ---
@paciente_bp.route('/perfil')
@login_required
@role_required('paciente')
def ver_perfil():
    usuario_nombre = session.get('usuario')
    paciente = PacienteDAO.get_by_nombreUsuario(usuario_nombre)
    usuario = UsuarioDAO.get_by_nombreUsuario(usuario_nombre)

    # Cargar fechaNacimiento y telefono desde Usuarios
    db = Database()
    conn = db.get_connection()
    if conn and usuario:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT fechaNacimiento, telefono FROM Usuarios WHERE nombreUsuario = ?",
                (usuario_nombre,)
            )
            row = cursor.fetchone()
            if row:
                if row[0]:
                    usuario.fechaNacimiento = row[0]
                if row[1]:
                    usuario.telefono = row[1]
        except:
            pass
        finally:
            cursor.close()

    # Cargar contactos
    familiares = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Nombre, Relacion, Telefono FROM Familiares WHERE Paciente = ?",
                (usuario_nombre,)
            )
            rows = cursor.fetchall()
            familiares = [
                {'nombre': r[0], 'relacion': r[1], 'telefono': r[2]}
                for r in rows
            ]
        except:
            pass
        finally:
            if 'cursor' in locals():
                cursor.close()

    return render_template('paciente/perfil.html',
                         usuario=usuario,
                         paciente=paciente,
                         familiares=familiares)