from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

# Importamos los DAOs que nos has facilitado
from app.dao.paciente_dao import PacienteDAO
from app.dao.otros_dao import ComentarioDAO, FamiliarDAO

# Importamos los Modelos para poder instanciar objetos
from app.models.comentarios import Comentario
from app.models.familiar import Familiar 

trabajador_bp = Blueprint('trabajador', __name__)

# 1. MENÚ PRINCIPAL / DASHBOARD DEL TRABAJADOR
@trabajador_bp.route('/trabajador/dashboard')
def dashboard():
    # Obtenemos la lista base de pacientes
    pacientes = PacienteDAO.get_all()
    
    # lo dejamos preparado para mostrar un saludo personalizado en la plantilla.
    nombre_empleado = session.get('nombre', 'Trabajador')
    
    return render_template('trabajador/dashboard.html', pacientes=pacientes, nombre_empleado=nombre_empleado)


# 2. EXPEDIENTE Y HISTORIAL DEL PACIENTE
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>')
def detalle_paciente(nombreUsuario):
    # Buscamos los datos del paciente
    paciente = PacienteDAO.get_by_nombreUsuario(nombreUsuario)
    if not paciente:
        flash('El paciente solicitado no existe en el sistema.', 'danger')
        return redirect(url_for('trabajador.dashboard'))
    
    # Línea de tiempo cronológica (Notas Clínicas de texto libre)
    notas_clinicas = ComentarioDAO.get_by_paciente(nombreUsuario)
    
    # Consultar contactos de emergencia del paciente
    contactos_emergencia = FamiliarDAO.get_by_paciente(nombreUsuario)
    
    return render_template(
        'trabajador/paciente_detalle.html', 
        paciente=paciente, 
        notas=notas_clinicas, 
        contactos=contactos_emergencia
    )


# 3. AÑADIR ANOTACIÓN DE FORMATO LIBRE (MÍNIMO 5 CARACTERES)
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/nota', methods=['POST'])
def nueva_nota(nombreUsuario):
    texto_nota = request.form.get('nota_texto')
    
    # VALIDACIÓN COMPULSORIA CU-09: Comprobar longitud mínima de 5 caracteres
    if not texto_nota or len(texto_nota.strip()) < 5:
        flash('Error: La anotación clínica debe tener un contenido mínimo de 5 caracteres.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))
    
    # Capturamos el usuario del trabajador logueado desde la sesión de Flask
    # Si no existiera en sesión por pruebas, usamos un valor por defecto seguro
    auxiliar_actual = session.get('usuario')
    
    # Creamos el objeto Comentario con el modelo que me has pasado
    nuevo_comentario = Comentario(
        Auxiliar=auxiliar_actual,
        Paciente=nombreUsuario,
        dia=datetime.now().date(), # Fecha de hoy
        nota=texto_nota.strip()
    )
    
    # Guardamos en la base de datos usando tu ComentarioDAO
    if ComentarioDAO.create(nuevo_comentario):
        flash('Anotación clínica registrada en el historial correctamente.', 'success')
    else:
        flash('Error crítico: No se pudo guardar la anotación en la base de datos.', 'danger')
        
    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))


# 4. AÑADIR CONTACTO DE EMERGENCIA
@trabajador_bp.route('/trabajador/paciente/<nombreUsuario>/contacto', methods=['POST'])
def nuevo_contacto(nombreUsuario):
    nombre = request.form.get('nombre_contacto')
    relacion = request.form.get('relacion_contacto')
    telefono = request.form.get('telefono_contacto')
    
    if not nombre or not relacion or not telefono:
        flash('Error: Todos los campos del contacto de emergencia son obligatorios.', 'warning')
        return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))
    
    # Creamos el objeto Familiar (asumiendo que los argumentos del constructor coinciden)
    nuevo_fam = Familiar(
        Nombre=nombre,
        Paciente=nombreUsuario,
        Relacion=relacion,
        Telefono=telefono
    )
    
    # Guardamos en la base de datos usando tu FamiliarDAO
    if FamiliarDAO.create(nuevo_fam):
        flash('Contacto de emergencia añadido con éxito.', 'success')
    else:
        flash('Error: No se pudo registrar el contacto familiar.', 'danger')
        
    return redirect(url_for('trabajador.detalle_paciente', nombreUsuario=nombreUsuario))