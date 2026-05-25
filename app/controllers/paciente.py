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

    print("\n=== DEPURACIÓN: RESPUESTAS RECIBIDAS ===")
    for key, valor in request.form.items():
        print(f"  {key} = {valor}")
    print("========================================\n")

    # Obtener respuestas del formulario
    respuesta_1 = request.form.get('respuesta_1', '').strip()  # ¿Cómo te encuentras hoy?
    respuesta_2 = request.form.get('respuesta_2', '').strip()  # ¿Cuántas horas has dormido?
    respuesta_3_si_no = request.form.get('respuesta_3_si_no', '')  # Sí/No
    respuesta_3_texto = request.form.get('respuesta_3', '').strip()  # ¿Qué hiciste?
    respuesta_4 = request.form.get('respuesta_4', '').strip()  # ¿Qué has desayunado?

    print(f"🔍 Pregunta 3 - Si/No: '{respuesta_3_si_no}', Texto: '{respuesta_3_texto}'")

    # Procesar respuesta 3
    if respuesta_3_si_no == 'Si':
        contenido_3 = f"Sí - {respuesta_3_texto}" if respuesta_3_texto else "Sí (sin descripción)"
    else:
        contenido_3 = "No"

    print(f"📝 Contenido final pregunta 3: '{contenido_3}'")

    # Validar que no haya respuestas vacías
    if not respuesta_1:
        flash('Por favor, indica cómo te encuentras hoy.', 'danger')
        return redirect(url_for('paciente.cuestionario'))
    if not respuesta_2:
        flash('Por favor, indica cuántas horas has dormido.', 'danger')
        return redirect(url_for('paciente.cuestionario'))
    if not respuesta_3_si_no:
        flash('Por favor, indica si recuerdas qué hiciste ayer.', 'danger')
        return redirect(url_for('paciente.cuestionario'))
    if not respuesta_4:
        flash('Por favor, indica qué has desayunado.', 'danger')
        return redirect(url_for('paciente.cuestionario'))

    # Mapeo de preguntas con IDs 1, 2, 3, 4 (BD limpia)
    respuestas_a_guardar = [
        (1, respuesta_1),   # ¿Cómo te encuentras hoy?
        (2, respuesta_2),   # ¿Cuántas horas has dormido?
        (3, contenido_3),   # ¿Recuerdas qué hiciste ayer por la tarde?
        (4, respuesta_4),   # ¿Qué has desayunado hoy?
    ]

    print("\n📋 RESUMEN DE RESPUESTAS A GUARDAR:")
    for id_preg, cont in respuestas_a_guardar:
        print(f"  ID {id_preg}: '{cont}'")
    print()

    errores = False
    for id_pregunta, contenido in respuestas_a_guardar:
        if not contenido:
            continue
        
        print(f"💾 Guardando pregunta ID {id_pregunta}: '{contenido}'")
        
        nueva_respuesta = Respuesta(
            idPregunta=id_pregunta,
            idPaciente=username,
            fechaHora=ahora,
            contenido=contenido
        )
        
        resultado = RespuestaDAO.create(nueva_respuesta)
        
        if not resultado:
            print(f"❌ Error al guardar pregunta ID {id_pregunta}")
            errores = True
        else:
            print(f"✅ Pregunta ID {id_pregunta} guardada correctamente (ID respuesta: {resultado})")

    if errores:
        flash('Hubo un error al guardar algunas respuestas. Inténtalo de nuevo.', 'danger')
    else:
        flash('¡Cuestionario enviado con éxito! Gracias.', 'success')

    return redirect(url_for('paciente.dashboard'))


# --- HISTORIAL DE RESPUESTAS DEL PACIENTE (NUEVO) ---
@paciente_bp.route('/historial')
@login_required
@role_required('paciente')
def historial():
    username = session.get('usuario')

    respuestas = RespuestaDAO.get_by_paciente(username)

    historial_agrupado = {}
    for r in respuestas:
        fecha = r.fechaHora.date() if r.fechaHora else None
        if fecha not in historial_agrupado:
            historial_agrupado[fecha] = []
        historial_agrupado[fecha].append(r)

    preguntas_dict = {}
    try:
        cuestionarios = CuestionarioDAO.get_all()
        for c in cuestionarios:
            preguntas = PreguntaDAO.get_by_cuestionario(c.idCuestionario)
            for p in preguntas:
                preguntas_dict[p.idPregunta] = p.enunciado
    except Exception as e:
        print(f"Error cargando preguntas en historial: {e}")

    return render_template('paciente/historial.html',
                           historial_agrupado=historial_agrupado,
                           preguntas_dict=preguntas_dict)


# --- VER PERFIL DEL PACIENTE (SOLO LECTURA - TU VERSIÓN) ---
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