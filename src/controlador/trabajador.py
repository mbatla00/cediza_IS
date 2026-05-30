from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
import re
from src.modelo.dao import Database #OJO!!! Database no se usa fuera del modelo
from .auth import login_required, role_required

from src.modelo.dao import PacienteDAO, ComentarioDAO, FacturaDAO, EvaluacionProfesionalDAO
from src.modelo.vo import Comentario, Familiar, EvaluacionProfesional

trabajador_bp = Blueprint('trabajador', __name__)


# --- DASHBOARD ---
@trabajador_bp.route('/trabajador/dashboard')
@login_required
@role_required('trabajador')
def dashboard():
    pacientes = PacienteDAO.get_all()
    nombre_empleado = session.get('nombre', 'Trabajador')
    
    usuario_actual = session.get('usuario')
    tipo_trabajador = None
    
    db = Database()
    conn = db.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                (usuario_actual,)
            )
            row = cursor.fetchone()
            if row:
                tipo_trabajador = row[0]
        except Exception as e:
            print(f"Error al obtener tipo de trabajador: {e}")
        finally:
            cursor.close()
    
    return render_template('trabajador/dashboard.html', 
                         pacientes=pacientes, 
                         nombre_empleado=nombre_empleado,
                         tipo_trabajador=tipo_trabajador)


# --- DETALLE DEL PACIENTE ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>')
@login_required
@role_required('trabajador')
def detalle_paciente(nombreUsuario):
    paciente = PacienteDAO.get_by_nombreUsuario(nombreUsuario)
    if not paciente:
        flash('El paciente solicitado no existe en el sistema.', 'danger')
        return redirect(url_for('trabajador.dashboard'))

    db = Database()
    conn = db.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT telefono, fechaNacimiento FROM Usuarios WHERE nombreUsuario = ?",
                (nombreUsuario,)
            )
            row = cursor.fetchone()
            if row:
                if row[0]:
                    paciente.telefono = row[0]
                if row[1]:
                    paciente.fechaNacimiento = row[1]
        except:
            pass
        finally:
            cursor.close()

    notas_clinicas = ComentarioDAO.get_by_paciente(nombreUsuario)
    contactos_emergencia = FamiliarDAO.get_by_paciente(nombreUsuario)
    evaluaciones = EvaluacionProfesionalDAO.get_by_paciente(nombreUsuario)

    # Cargar sesiones del paciente
    from app.dao.otros_dao import SesionDAO
    sesiones_paciente = SesionDAO.get_by_paciente(nombreUsuario)

    # Separar sesiones en próximas y pasadas
    sesiones_proximas_paciente = []
    sesiones_pasadas_paciente = []
    hoy = date.today()
    hora_actual = datetime.now().time()

    for s in sesiones_paciente:
        fecha_sesion = s.fecha
        hora_sesion = s.hora
        
        if fecha_sesion and fecha_sesion > hoy:
            sesiones_proximas_paciente.append(s)
        elif fecha_sesion and fecha_sesion < hoy:
            sesiones_pasadas_paciente.append(s)
        elif fecha_sesion == hoy:
            if hora_sesion and hora_sesion > hora_actual:
                sesiones_proximas_paciente.append(s)
            else:
                sesiones_pasadas_paciente.append(s)
        else:
            sesiones_pasadas_paciente.append(s)

    return render_template(
        'trabajador/paciente_detalle.html',
        paciente=paciente,
        notas=notas_clinicas,
        contactos=contactos_emergencia,
        evaluaciones=evaluaciones,
        sesiones_proximas_paciente=sesiones_proximas_paciente,
        sesiones_pasadas_paciente=sesiones_pasadas_paciente
    )


# --- EDITAR DATOS DEL PACIENTE ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/editar', methods=['POST'])
@login_required
@role_required('trabajador')
def editar_paciente(nombreUsuario):
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    diagnostico = request.form.get('diagnostico')

    db = Database()
    conn = db.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Usuarios
                SET Nombre = ?, email = ?, fechaNacimiento = ?, telefono = ?
                WHERE nombreUsuario = ?
            """, (nombre, email, fecha_nacimiento or None, telefono, nombreUsuario))
            cursor.execute("""
                UPDATE Pacientes SET diagnostico = ? WHERE nombreUsuario = ?
            """, (diagnostico, nombreUsuario))
            conn.commit()
            flash('Datos del paciente actualizados correctamente.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar: {e}', 'danger')
        finally:
            cursor.close()

    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# --- AÑADIR ANOTACIÓN CLÍNICA ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/nota', methods=['POST'])
@login_required
@role_required('trabajador')
def nueva_nota(nombreUsuario):
    texto_nota = request.form.get('nota_texto')
    hora_actual = datetime.now().time()

    if not texto_nota or len(texto_nota.strip()) < 5:
        flash('Error: La anotación clínica debe tener un contenido mínimo de 5 caracteres.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))

    auxiliar_actual = session.get('usuario')

    nuevo_comentario = Comentario(
        Auxiliar=auxiliar_actual,
        Paciente=nombreUsuario,
        dia=datetime.now().date(),
        hora=hora_actual,
        nota=texto_nota.strip()
    )

    if ComentarioDAO.create(nuevo_comentario):
        flash('Anotación clínica registrada en el historial correctamente.', 'success')
    else:
        flash('Error crítico: No se pudo guardar la anotación en la base de datos.', 'danger')

    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# --- AÑADIR CONTACTO DE EMERGENCIA ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/contacto', methods=['POST'])
@login_required
@role_required('trabajador')
def nuevo_contacto(nombreUsuario):
    nombre = request.form.get('nombre_contacto')
    relacion = request.form.get('relacion_contacto')
    telefono = request.form.get('telefono_contacto')

    if not nombre or not relacion or not telefono:
        flash('Error: Todos los campos del contacto de emergencia son obligatorios.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))

    if not re.match(r'^\d{9}$', telefono):
        flash('Error: El teléfono debe tener exactamente 9 dígitos, sin espacios ni letras.', 'danger')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))

    nuevo_fam = Familiar(
        Nombre=nombre,
        Paciente=nombreUsuario,
        Relacion=relacion,
        Telefono=telefono
    )

    if FamiliarDAO.create(nuevo_fam):
        flash('Contacto de emergencia añadido con éxito.', 'success')
    else:
        flash('Error: No se pudo registrar el contacto familiar.', 'danger')

    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# --- MOSTRAR FORMULARIO DE EVALUACIÓN RÁPIDA ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/evaluar')
@login_required
@role_required('trabajador')
def evaluar_paciente(nombreUsuario):
    hoy = date.today()
    evaluaciones_hoy = EvaluacionProfesionalDAO.get_by_paciente(nombreUsuario)
    ya_evaluo_hoy = False
    
    for e in evaluaciones_hoy:
        if hasattr(e, 'fecha'):
            fecha_eval = e.fecha
            if isinstance(fecha_eval, str):
                try:
                    fecha_eval = datetime.strptime(fecha_eval, '%Y-%m-%d').date()
                except:
                    try:
                        fecha_eval = datetime.strptime(fecha_eval, '%Y-%m-%d %H:%M:%S').date()
                    except:
                        continue
            elif isinstance(fecha_eval, datetime):
                fecha_eval = fecha_eval.date()
            
            if fecha_eval == hoy:
                ya_evaluo_hoy = True
                break
    
    if ya_evaluo_hoy:
        flash('Este paciente ya ha sido evaluado hoy. Solo se permite una evaluación por día.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))
    
    paciente = PacienteDAO.get_by_nombreUsuario(nombreUsuario)
    if not paciente:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    return render_template('trabajador/evaluar_paciente.html', paciente=paciente)


# --- GUARDAR EVALUACIÓN RÁPIDA ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/evaluacion', methods=['POST'])
@login_required
@role_required('trabajador')
def guardar_evaluacion(nombreUsuario):
    trabajador = session.get('usuario')
    
    hoy = date.today()
    evaluaciones_hoy = EvaluacionProfesionalDAO.get_by_paciente(nombreUsuario)
    ya_evaluo_hoy = False
    
    for e in evaluaciones_hoy:
        if hasattr(e, 'fecha'):
            fecha_eval = e.fecha
            if isinstance(fecha_eval, str):
                try:
                    fecha_eval = datetime.strptime(fecha_eval, '%Y-%m-%d').date()
                except:
                    try:
                        fecha_eval = datetime.strptime(fecha_eval, '%Y-%m-%d %H:%M:%S').date()
                    except:
                        continue
            elif isinstance(fecha_eval, datetime):
                fecha_eval = fecha_eval.date()
            
            if fecha_eval == hoy:
                ya_evaluo_hoy = True
                break
    
    if ya_evaluo_hoy:
        flash('Este paciente ya ha sido evaluado hoy. Solo se permite una evaluación por día.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))
    
    estadoEmocional = request.form.get('estadoEmocional')
    movilidad = request.form.get('movilidad')
    apetito = request.form.get('apetito')
    observaciones = request.form.get('observaciones', '').strip()
    
    if not estadoEmocional or not movilidad or not apetito:
        flash('Todos los campos obligatorios deben estar marcados.', 'danger')
        return redirect(url_for('trabajador.evaluar_paciente', nombreUsuario=nombreUsuario))
    
    nueva_evaluacion = EvaluacionProfesional(
        Paciente=nombreUsuario,
        Trabajador=trabajador,
        fecha=hoy,
        movilidad=int(movilidad),
        estadoEmocional=int(estadoEmocional),
        apetito=int(apetito),
        observaciones=observaciones
    )
    
    if EvaluacionProfesionalDAO.create(nueva_evaluacion):
        flash('Evaluación guardada correctamente.', 'success')
    else:
        flash('Error al guardar la evaluación.', 'danger')
    
    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# ============== SECCIÓN ESPECIALISTA ==============

# --- DASHBOARD ESPECIALISTA ---
@trabajador_bp.route('/especialista/dashboard')
@login_required
@role_required('trabajador')
def especialista_dashboard():
    usuario_actual = session.get('usuario')
    ahora = datetime.now()
    hoy = ahora.date()
    hora_actual = ahora.time()
    
    db = Database()
    conn = db.get_connection()
    es_especialista = False
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                (usuario_actual,)
            )
            row = cursor.fetchone()
            if row and row[0] == 'especialista':
                es_especialista = True
        except:
            pass
        finally:
            cursor.close()
    
    if not es_especialista:
        flash('Acceso solo para especialistas.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    from app.dao.otros_dao import SesionDAO
    todas_sesiones = SesionDAO.get_by_especialista(usuario_actual)
    
    sesiones_proximas = []
    sesiones_pasadas = []
    
    for s in todas_sesiones:
        fecha_sesion = s.fecha
        if isinstance(fecha_sesion, str):
            fecha_sesion = datetime.strptime(fecha_sesion, '%Y-%m-%d').date()
        
        hora_sesion = s.hora
        if isinstance(hora_sesion, str):
            try:
                hora_sesion = datetime.strptime(hora_sesion, '%H:%M:%S').time()
            except ValueError:
                hora_sesion = datetime.strptime(hora_sesion, '%H:%M').time()
        
        if fecha_sesion and fecha_sesion > hoy:
            sesiones_proximas.append(s)
        elif fecha_sesion and fecha_sesion < hoy:
            sesiones_pasadas.append(s)
        elif fecha_sesion == hoy:
            if hora_sesion and hora_actual and hora_sesion > hora_actual:
                sesiones_proximas.append(s)
            else:
                sesiones_pasadas.append(s)
        else:
            sesiones_proximas.append(s)
    
    sesiones_proximas.sort(
        key=lambda x: (x.fecha, x.hora if x.hora else datetime.strptime('00:00:00', '%H:%M:%S').time())
    )
    sesiones_pasadas.sort(
        key=lambda x: (x.fecha, x.hora if x.hora else datetime.strptime('00:00:00', '%H:%M:%S').time()),
        reverse=True
    )
    
    pacientes = PacienteDAO.get_all()
    
    return render_template('trabajador/especialista_dashboard.html', 
                         sesiones_proximas=sesiones_proximas,
                         sesiones_pasadas=sesiones_pasadas,
                         pacientes=pacientes,
                         nombre_especialista=session.get('nombre', 'Especialista'))


# --- CREAR NUEVA SESIÓN ---
@trabajador_bp.route('/especialista/crear-sesion', methods=['POST'])
@login_required
@role_required('trabajador')
def crear_sesion():
    especialista = session.get('usuario')
    
    db = Database()
    conn = db.get_connection()
    es_especialista = False
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                (especialista,)
            )
            row = cursor.fetchone()
            if row and row[0] == 'especialista':
                es_especialista = True
        except:
            pass
        finally:
            cursor.close()
    
    if not es_especialista:
        flash('Acceso solo para especialistas.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    paciente = request.form.get('paciente')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    comentarios = request.form.get('comentarios', '').strip()
    
    if not paciente or not fecha or not hora:
        flash('Paciente, fecha y hora son obligatorios.', 'danger')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    from app.dao.otros_dao import SesionDAO
    from app.models.sesion import Sesion
    
    nueva_sesion = Sesion(
        Paciente=paciente,
        Especialista=especialista,
        comentarios=comentarios,
        Fecha=fecha,
        Hora=hora
    )
    
    resultado = SesionDAO.create(nueva_sesion)
    if resultado:
        flash('Sesión creada correctamente.', 'success')
    else:
        flash('Error al crear la sesión.', 'danger')
    
    return redirect(url_for('trabajador.especialista_dashboard'))


# --- EDITAR SESIÓN ---
@trabajador_bp.route('/especialista/editar-sesion/<int:idSesion>', methods=['GET', 'POST'])
@login_required
@role_required('trabajador')
def editar_sesion(idSesion):
    usuario_actual = session.get('usuario')
    
    db = Database()
    conn = db.get_connection()
    es_especialista = False
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                (usuario_actual,)
            )
            row = cursor.fetchone()
            if row and row[0] == 'especialista':
                es_especialista = True
        except:
            pass
        finally:
            cursor.close()
    
    if not es_especialista:
        flash('Acceso solo para especialistas.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    from app.dao.otros_dao import SesionDAO
    sesion = SesionDAO.get_by_id(idSesion)
    
    if not sesion:
        flash('Sesión no encontrada.', 'danger')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    if sesion.especialista != usuario_actual:
        flash('No puedes editar sesiones de otro especialista.', 'danger')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        comentarios = request.form.get('comentarios', '').strip()
        
        if not fecha or not hora:
            flash('Fecha y hora son obligatorios.', 'danger')
            return redirect(url_for('trabajador.editar_sesion', idSesion=idSesion))
        
        sesion.fecha = fecha
        sesion.hora = hora
        sesion.comentarios = comentarios
        
        if SesionDAO.update(sesion):
            flash('Sesión actualizada correctamente.', 'success')
        else:
            flash('Error al actualizar la sesión.', 'danger')
        
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    pacientes = PacienteDAO.get_all()
    return render_template('trabajador/editar_sesion.html', 
                         sesion=sesion,
                         pacientes=pacientes)


# --- ELIMINAR SESIÓN ---
@trabajador_bp.route('/especialista/eliminar-sesion/<int:idSesion>', methods=['POST'])
@login_required
@role_required('trabajador')
def eliminar_sesion(idSesion):
    usuario_actual = session.get('usuario')
    
    db = Database()
    conn = db.get_connection()
    es_especialista = False
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                (usuario_actual,)
            )
            row = cursor.fetchone()
            if row and row[0] == 'especialista':
                es_especialista = True
        except:
            pass
        finally:
            cursor.close()
    
    if not es_especialista:
        flash('Acceso solo para especialistas.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    from app.dao.otros_dao import SesionDAO
    sesion = SesionDAO.get_by_id(idSesion)
    
    if not sesion:
        flash('Sesión no encontrada.', 'danger')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    if sesion.especialista != usuario_actual:
        flash('No puedes eliminar sesiones de otro especialista.', 'danger')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    ahora = datetime.now()
    fecha_sesion = sesion.fecha
    if isinstance(fecha_sesion, str):
        fecha_sesion = datetime.strptime(fecha_sesion, '%Y-%m-%d').date()
    
    hora_sesion = sesion.hora
    if isinstance(hora_sesion, str):
        try:
            hora_sesion = datetime.strptime(hora_sesion, '%H:%M:%S').time()
        except:
            hora_sesion = datetime.strptime(hora_sesion, '%H:%M').time()
    
    if fecha_sesion < ahora.date():
        flash('No se pueden eliminar sesiones pasadas.', 'warning')
        return redirect(url_for('trabajador.especialista_dashboard'))
    elif fecha_sesion == ahora.date() and hora_sesion and hora_sesion < ahora.time():
        flash('No se pueden eliminar sesiones que ya han comenzado.', 'warning')
        return redirect(url_for('trabajador.especialista_dashboard'))
    
    if SesionDAO.delete(idSesion):
        flash('Sesión eliminada correctamente.', 'success')
    else:
        flash('Error al eliminar la sesión.', 'danger')
    
    return redirect(url_for('trabajador.especialista_dashboard'))


# --- VER SESIONES DEL PACIENTE ---
@trabajador_bp.route('/especialista/paciente/<nombreUsuario>/sesiones')
@login_required
@role_required('trabajador')
def ver_sesiones_paciente(nombreUsuario):
    from app.dao.otros_dao import SesionDAO
    sesiones = SesionDAO.get_by_paciente(nombreUsuario)
    paciente = PacienteDAO.get_by_nombreUsuario(nombreUsuario)
    
    return render_template('trabajador/especialista_sesiones_paciente.html',
                         sesiones=sesiones,
                         paciente=paciente)