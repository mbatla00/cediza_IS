from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import re
from app.dao.database import Database

from app.dao.paciente_dao import PacienteDAO
from app.dao.otros_dao import ComentarioDAO, FamiliarDAO
from app.models.comentarios import Comentario
from app.models.familiar import Familiar

trabajador_bp = Blueprint('trabajador', __name__)


# --- DASHBOARD ---
@trabajador_bp.route('/trabajador/dashboard')
def dashboard():
    pacientes = PacienteDAO.get_all()
    nombre_empleado = session.get('nombre', 'Trabajador')
    return render_template('trabajador/dashboard.html', pacientes=pacientes, nombre_empleado=nombre_empleado)


# --- DETALLE DEL PACIENTE ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>')
def detalle_paciente(nombreUsuario):
    paciente = PacienteDAO.get_by_nombreUsuario(nombreUsuario)
    if not paciente:
        flash('El paciente solicitado no existe en el sistema.', 'danger')
        return redirect(url_for('trabajador.dashboard'))

    # Cargar teléfono y fechaNacimiento desde Usuarios
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

    return render_template(
        'trabajador/paciente_detalle.html',
        paciente=paciente,
        notas=notas_clinicas,
        contactos=contactos_emergencia
    )


# --- EDITAR DATOS DEL PACIENTE (SIN CUENTA BANCARIA) ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/editar', methods=['POST'])
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
def nueva_nota(nombreUsuario):
    texto_nota = request.form.get('nota_texto')

    if not texto_nota or len(texto_nota.strip()) < 5:
        flash('Error: La anotación clínica debe tener un contenido mínimo de 5 caracteres.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))

    auxiliar_actual = session.get('usuario')

    nuevo_comentario = Comentario(
        Auxiliar=auxiliar_actual,
        Paciente=nombreUsuario,
        dia=datetime.now().date(),
        nota=texto_nota.strip()
    )

    if ComentarioDAO.create(nuevo_comentario):
        flash('Anotación clínica registrada en el historial correctamente.', 'success')
    else:
        flash('Error crítico: No se pudo guardar la anotación en la base de datos.', 'danger')

    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# --- AÑADIR CONTACTO DE EMERGENCIA ---
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/contacto', methods=['POST'])
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