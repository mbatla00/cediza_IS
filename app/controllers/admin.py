from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth import login_required, role_required
from app.dao.paciente_dao import PacienteDAO, PacPubDAO, PacPriDAO
from app.models.paciente_tipos import PacPub, PacPri
from app.dao.usuario_dao import UsuarioDAO
from app.models.usuario import Usuario
from app.dao.otros_dao import FamiliarDAO
from app.models.familiar import Familiar
from app.dao.database import Database
import re

admin_bp = Blueprint('admin', __name__)


# --- DASHBOARD ---
@admin_bp.route('/admin/dashboard')
@login_required
@role_required('admin')
def dashboard():
    return render_template('admin/dashboard.html')


# --- ALTA DE PACIENTE ---
@admin_bp.route('/admin/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def nuevo_paciente():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo')
        dni = request.form.get('dni')
        email = request.form.get('email')
        fecha_nacimiento_input = request.form.get('fecha_nacimiento')
        telefono = request.form.get('telefono')
        tipo = request.form.get('tipo')
        cuenta = request.form.get('cuenta')
        nombre_usuario_manual = request.form.get('nombre_usuario_manual')
        password = request.form.get('password', dni)

        fecha_nacimiento = fecha_nacimiento_input if fecha_nacimiento_input and fecha_nacimiento_input.strip() else None

        if nombre_usuario_manual and nombre_usuario_manual.strip():
            nombre_usuario = nombre_usuario_manual.strip().replace(' ', '').lower()[:50]
        else:
            nombre_usuario = nombre_completo.replace(' ', '').lower()[:50]

        # VALIDACIONES
        
        # 1. Validar DNI
        if not UsuarioDAO.validar_dni(dni):
            flash('El DNI introducido no es válido.', 'danger')
            return redirect(url_for('admin.nuevo_paciente'))
        
        # 2. Validar teléfono principal (si no está vacío)
        if telefono and telefono.strip():
            if not re.match(r'^\d{9}$', telefono):
                flash('El teléfono debe tener exactamente 9 dígitos, sin espacios.', 'danger')
                return redirect(url_for('admin.nuevo_paciente'))
        
        # 3. Validar teléfonos de contactos
        contacto_telefonos = request.form.getlist('contacto_telefono')
        for telefono_c in contacto_telefonos:
            if telefono_c and telefono_c.strip():
                if not re.match(r'^\d{9}$', telefono_c):
                    flash('Los teléfonos de contacto deben tener exactamente 9 dígitos, sin espacios.', 'danger')
                    return redirect(url_for('admin.nuevo_paciente'))
        
        # 4. Validar que no exista el usuario
        if UsuarioDAO.get_by_nombreUsuario(nombre_usuario):
            flash(f'El nombre de usuario "{nombre_usuario}" ya está ocupado.', 'warning')
            return redirect(url_for('admin.nuevo_paciente'))
        
        # 5. Validar que no exista el DNI
        if UsuarioDAO.get_by_dni(dni):
            flash(f'Ya existe un usuario con el DNI {dni}.', 'danger')
            return redirect(url_for('admin.nuevo_paciente'))

        # Si llegamos aquí, todas las validaciones pasaron
        try:
            nuevo_usuario = Usuario(
                nombreUsuario=nombre_usuario,
                Nombre=nombre_completo,
                DNI=dni,
                Rol='paciente',
                password=password,
                email=email,
                fechaNacimiento=fecha_nacimiento
            )

            if not UsuarioDAO.create(nuevo_usuario):
                flash('Error al crear la cuenta de usuario base.', 'danger')
                return redirect(url_for('admin.nuevo_paciente'))

            # Guardar teléfono en Usuarios
            if telefono:
                db = Database()
                conn = db.get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE Usuarios SET telefono = ? WHERE nombreUsuario = ?",
                            (telefono, nombre_usuario)
                        )
                        conn.commit()
                    except Exception as e:
                        print(f"Error al guardar teléfono: {e}")
                    finally:
                        cursor.close()

            if tipo == 'publico':
                nuevo_p = PacPub(
                    nombreUsuario=nombre_usuario,
                    Nombre=nombre_completo,
                    DNI=dni,
                    password=password,
                    Dias_ingresado=0,
                    email=email
                )
                exito = PacienteDAO.create(nuevo_p) and PacPubDAO.create(nuevo_p)
            else:
                if not cuenta:
                    flash('Los pacientes privados necesitan cuenta bancaria.', 'warning')
                    return redirect(url_for('admin.nuevo_paciente'))
                nuevo_p = PacPri(
                    nombreUsuario=nombre_usuario,
                    Nombre=nombre_completo,
                    DNI=dni,
                    password=password,
                    cuenta=cuenta,
                    email=email
                )
                exito = PacienteDAO.create(nuevo_p) and PacPriDAO.create(nuevo_p)

            if not exito:
                flash('Error al guardar datos del paciente.', 'danger')
                return redirect(url_for('admin.nuevo_paciente'))

            # Guardar enfermedades y contactos
            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    # Enfermedades seleccionadas
                    enfermedades_ids = request.form.getlist('enfermedades')
                    for enf_id in enfermedades_ids:
                        if not enf_id.startswith('nueva_'):  # Solo IDs numéricos
                            cursor.execute(
                                "INSERT INTO PacienteEnfermedad (paciente, enfermedad_id) VALUES (?, ?)",
                                (nombre_usuario, enf_id)
                            )
                    
                    # Otra enfermedad
                    otra = request.form.get('otra_enfermedad')
                    if otra and otra.strip():
                        cursor.execute("INSERT INTO Enfermedades (nombre) VALUES (?)", (otra.strip(),))
                        conn.commit()
                        nuevo_id = cursor.lastrowid
                        cursor.execute(
                            "INSERT INTO PacienteEnfermedad (paciente, enfermedad_id) VALUES (?, ?)",
                            (nombre_usuario, nuevo_id)
                        )

                    # Contactos de emergencia (múltiples)
                    contacto_nombres = request.form.getlist('contacto_nombre')
                    contacto_relaciones = request.form.getlist('contacto_relacion')
                    contacto_telefonos = request.form.getlist('contacto_telefono')

                    for i in range(len(contacto_nombres)):
                        nombre_c = contacto_nombres[i].strip() if i < len(contacto_nombres) else ''
                        relacion_c = contacto_relaciones[i].strip() if i < len(contacto_relaciones) else ''
                        telefono_c = contacto_telefonos[i].strip() if i < len(contacto_telefonos) else ''
                        if nombre_c and telefono_c:
                            cursor.execute(
                                "INSERT INTO Familiares (Nombre, Paciente, Relacion, Telefono) VALUES (?, ?, ?, ?)",
                                (nombre_c, nombre_usuario, relacion_c, telefono_c)
                            )

                    conn.commit()
                except Exception as e:
                    print(f"Error al guardar enfermedades/contactos: {e}")
                    conn.rollback()
                finally:
                    cursor.close()

            flash(f'Paciente {nombre_completo} registrado correctamente.', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            flash(f'Error crítico: {str(e)}', 'danger')
            return redirect(url_for('admin.nuevo_paciente'))

    # GET: Cargar enfermedades
    db = Database()
    conn = db.get_connection()
    enfermedades = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Enfermedades ORDER BY nombre")
            rows = cursor.fetchall()
            enfermedades = [{'id': r[0], 'nombre': r[1]} for r in rows]
        except Exception as e:
            print(f"Error cargando enfermedades: {e}")
        finally:
            cursor.close()

    return render_template('admin/paciente_form.html', enfermedades=enfermedades)


# --- ALTA DE TRABAJADOR ---
@admin_bp.route('/admin/trabajadores/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def nuevo_trabajador():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo')
        nombre_usuario = request.form.get('nombre_usuario').strip().lower()
        dni = request.form.get('dni')
        email = request.form.get('email')
        tipo = request.form.get('tipo')
        password = request.form.get('password')
        horario = request.form.get('horario')
        horario_especialista = request.form.get('horario_especialista')
        especialidad = request.form.get('especialidad')

        try:
            if not UsuarioDAO.validar_dni(dni):
                flash('El DNI introducido no es válido.', 'danger')
                return redirect(url_for('admin.nuevo_trabajador'))

            if UsuarioDAO.get_by_nombreUsuario(nombre_usuario):
                flash(f'El nombre de usuario "{nombre_usuario}" ya está ocupado.', 'warning')
                return redirect(url_for('admin.nuevo_trabajador'))

            nuevo_usr = Usuario(
                nombreUsuario=nombre_usuario,
                Nombre=nombre_completo,
                DNI=dni,
                Rol='trabajador',
                password=password,
                email=email
            )

            if not UsuarioDAO.create(nuevo_usr):
                flash('Error al crear la cuenta de usuario.', 'danger')
                return redirect(url_for('admin.nuevo_trabajador'))

            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO Trabajadores (nombreUsuario, Tipo) VALUES (?, ?)",
                        (nombre_usuario, tipo)
                    )

                    if tipo == 'auxiliar':
                        cursor.execute(
                            "INSERT INTO Auxiliares (nombreUsuario, Horario) VALUES (?, ?)",
                            (nombre_usuario, horario or 'Mañana')
                        )
                    elif tipo == 'coordinador':
                        cursor.execute(
                            "INSERT INTO coordinadores (nombreUsuario) VALUES (?)",
                            (nombre_usuario,)
                        )
                    elif tipo == 'especialista':
                        cursor.execute(
                            "INSERT INTO Especialistas (nombreUsuario, Especialidad, Horario) VALUES (?, ?, ?)",
                            (nombre_usuario, especialidad or '', horario or '')
                        )

                    conn.commit()
                    flash(f'Trabajador {nombre_completo} registrado correctamente.', 'success')
                except Exception as e:
                    conn.rollback()
                    flash(f'Error al guardar trabajador: {e}', 'danger')
                finally:
                    cursor.close()

            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            flash(f'Error crítico: {str(e)}', 'danger')
            return redirect(url_for('admin.nuevo_trabajador'))

    return render_template('admin/trabajador_form.html')


# --- LISTADO DE USUARIOS ---
@admin_bp.route('/admin/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    # Obtener todos los usuarios excepto el admin actual
    usuarios_bd = UsuarioDAO.get_all()
    # Filtrar para no mostrar al admin actual
    usuarios_filtrados = [u for u in usuarios_bd if u.nombreUsuario != session.get('usuario')]
    return render_template('admin/usuarios_lista.html', usuarios=usuarios_filtrados)


# --- EDITAR USUARIO ---
@admin_bp.route('/admin/usuarios/editar/<nombre_usuario>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_usuario(nombre_usuario):
    usuario = UsuarioDAO.get_by_nombreUsuario(nombre_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))

    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.email = request.form.get('email')
        usuario.dni = request.form.get('dni')
        usuario.fechaNacimiento = request.form.get('fecha_nacimiento') or None
        usuario.telefono = request.form.get('telefono')
        password = request.form.get('password')

        # Validar teléfono en edición
        if usuario.telefono and usuario.telefono.strip():
            if not re.match(r'^\d{9}$', usuario.telefono):
                flash('El teléfono debe tener exactamente 9 dígitos, sin espacios.', 'danger')
                return redirect(url_for('admin.editar_usuario', nombre_usuario=nombre_usuario))

        if password and password.strip():
            usuario.password = password.strip()

        if UsuarioDAO.update(usuario):
            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    # Guardar telefono y fechaNacimiento directo en Usuarios
                    cursor.execute(
                        "UPDATE Usuarios SET telefono = ?, fechaNacimiento = ? WHERE nombreUsuario = ?",
                        (usuario.telefono, usuario.fechaNacimiento, usuario.nombreUsuario)
                    )

                    if usuario.rol == 'paciente':
                        tipo_pac = request.form.get('tipo')
                        cursor.execute("UPDATE Pacientes SET Tipo = ? WHERE nombreUsuario = ?",
                                       (tipo_pac, usuario.nombreUsuario))

                        # Enfermedades
                        cursor.execute("DELETE FROM PacienteEnfermedad WHERE paciente = ?",
                                       (usuario.nombreUsuario,))
                        enfermedades_ids = request.form.getlist('enfermedades')
                        for enf_id in enfermedades_ids:
                            if not enf_id.startswith('nueva_'):
                                cursor.execute(
                                    "INSERT INTO PacienteEnfermedad (paciente, enfermedad_id) VALUES (?, ?)",
                                    (usuario.nombreUsuario, enf_id)
                                )
                        otra = request.form.get('otra_enfermedad')
                        if otra and otra.strip():
                            cursor.execute("INSERT INTO Enfermedades (nombre) VALUES (?)", (otra.strip(),))
                            conn.commit()
                            nuevo_id = cursor.lastrowid
                            cursor.execute(
                                "INSERT INTO PacienteEnfermedad (paciente, enfermedad_id) VALUES (?, ?)",
                                (usuario.nombreUsuario, nuevo_id)
                            )

                        # Contactos de emergencia
                        cursor.execute("DELETE FROM Familiares WHERE Paciente = ?",
                                       (usuario.nombreUsuario,))
                        contacto_nombres = request.form.getlist('contacto_nombre')
                        contacto_relaciones = request.form.getlist('contacto_relacion')
                        contacto_telefonos = request.form.getlist('contacto_telefono')

                        for i in range(len(contacto_nombres)):
                            nombre_c = contacto_nombres[i].strip() if i < len(contacto_nombres) else ''
                            relacion_c = contacto_relaciones[i].strip() if i < len(contacto_relaciones) else ''
                            telefono_c = contacto_telefonos[i].strip() if i < len(contacto_telefonos) else ''
                            if nombre_c and telefono_c:
                                if not re.match(r'^\d{9}$', telefono_c):
                                    flash('Los teléfonos de contacto deben tener exactamente 9 dígitos, sin espacios.', 'danger')
                                    return redirect(url_for('admin.editar_usuario', nombre_usuario=nombre_usuario))
                                cursor.execute(
                                    """INSERT INTO Familiares (Nombre, Paciente, Relacion, Telefono)
                                       VALUES (?, ?, ?, ?)""",
                                    (nombre_c, usuario.nombreUsuario, relacion_c, telefono_c)
                                )

                    elif usuario.rol == 'trabajador':
                        tipo_trab = request.form.get('tipo_trabajador')
                        horario = request.form.get('horario')
                        especialidad = request.form.get('especialidad')
                        
                        # Actualizar tipo en Trabajadores
                        cursor.execute("UPDATE Trabajadores SET Tipo = ? WHERE nombreUsuario = ?",
                                       (tipo_trab, usuario.nombreUsuario))
                        
                        # Eliminar de todas las tablas específicas primero
                        cursor.execute("DELETE FROM Auxiliares WHERE nombreUsuario = ?", (usuario.nombreUsuario,))
                        cursor.execute("DELETE FROM Especialistas WHERE nombreUsuario = ?", (usuario.nombreUsuario,))
                        cursor.execute("DELETE FROM coordinadores WHERE nombreUsuario = ?", (usuario.nombreUsuario,))
                        
                        # Insertar en la tabla correspondiente
                        if tipo_trab == 'auxiliar':
                            cursor.execute(
                                "INSERT INTO Auxiliares (nombreUsuario, Horario) VALUES (?, ?)",
                                (usuario.nombreUsuario, horario or 'Mañana')
                            )
                        elif tipo_trab == 'coordinador':
                            cursor.execute(
                                "INSERT INTO coordinadores (nombreUsuario) VALUES (?)",
                                (usuario.nombreUsuario,)
                            )
                        elif tipo_trab == 'especialista':
                            cursor.execute(
                                "INSERT INTO Especialistas (nombreUsuario, Especialidad, Horario) VALUES (?, ?, ?)",
                                (usuario.nombreUsuario, especialidad or '', horario_especialista or '')
                            )

                    conn.commit()
                except Exception as e:
                    print(f"Error al actualizar: {e}")
                    conn.rollback()
                finally:
                    cursor.close()

            flash('Usuario actualizado correctamente.', 'success')
        else:
            flash('Error al actualizar el usuario.', 'danger')

        return redirect(url_for('admin.listar_usuarios'))

    # GET: Cargar datos
    db = Database()
    conn = db.get_connection()
    enfermedades = []
    paciente_enfermedades = []
    contactos = []
    datos_trabajador = {}

    if conn:
        cursor = conn.cursor()
        try:
            # Cargar fechaNacimiento y telefono
            cursor.execute(
                "SELECT fechaNacimiento, telefono FROM Usuarios WHERE nombreUsuario = ?",
                (usuario.nombreUsuario,)
            )
            row = cursor.fetchone()
            if row:
                if row[0]:
                    usuario.fechaNacimiento = row[0]
                if row[1]:
                    usuario.telefono = row[1]

            # Enfermedades disponibles
            cursor.execute("SELECT * FROM Enfermedades ORDER BY nombre")
            rows = cursor.fetchall()
            enfermedades = [{'id': r[0], 'nombre': r[1]} for r in rows]

            # Enfermedades del paciente
            if usuario.rol == 'paciente':
                cursor.execute(
                    "SELECT enfermedad_id FROM PacienteEnfermedad WHERE paciente = ?",
                    (usuario.nombreUsuario,)
                )
                paciente_enfermedades = [r[0] for r in cursor.fetchall()]

            # Contactos
            cursor.execute(
                "SELECT Nombre, Relacion, Telefono FROM Familiares WHERE Paciente = ?",
                (usuario.nombreUsuario,)
            )
            rows = cursor.fetchall()
            contactos = [
                {'nombre': r[0], 'relacion': r[1], 'telefono': r[2]}
                for r in rows
            ]

            # Datos del trabajador
            if usuario.rol == 'trabajador':
                cursor.execute(
                    "SELECT Tipo FROM Trabajadores WHERE nombreUsuario = ?",
                    (usuario.nombreUsuario,)
                )
                row_trab = cursor.fetchone()
                if row_trab:
                    datos_trabajador['tipo'] = row_trab[0]
                    
                    if row_trab[0] == 'auxiliar':
                        cursor.execute(
                            "SELECT Horario FROM Auxiliares WHERE nombreUsuario = ?",
                            (usuario.nombreUsuario,)
                        )
                        row_aux = cursor.fetchone()
                        if row_aux:
                            datos_trabajador['horario'] = row_aux[0]
                            
                    elif row_trab[0] == 'especialista':
                        cursor.execute(
                            "SELECT Especialidad, Horario FROM Especialistas WHERE nombreUsuario = ?",
                            (usuario.nombreUsuario,)
                        )
                        row_esp = cursor.fetchone()
                        if row_esp:
                            datos_trabajador['especialidad'] = row_esp[0]
                            datos_trabajador['horario'] = row_esp[1]

        except Exception as e:
            print(f"Error al cargar datos: {e}")
        finally:
            cursor.close()

    return render_template('admin/editar_usuario.html',
                           usuario=usuario,
                           enfermedades=enfermedades,
                           paciente_enfermedades=paciente_enfermedades,
                           contactos=contactos,
                           datos_trabajador=datos_trabajador)


# --- GESTIÓN DE BAJAS ---
@admin_bp.route('/admin/usuarios/gestion-bajas')
@login_required
@role_required('admin')
def gestion_bajas():
    usuarios_bd = UsuarioDAO.get_all()
    # Filtrar para no mostrar al admin actual
    usuarios_filtrados = [u for u in usuarios_bd if u.nombreUsuario != session.get('usuario')]
    return render_template('admin/usuarios_lista.html', usuarios=usuarios_filtrados)


@admin_bp.route('/admin/usuarios/cambiar-estado/<nombre_usuario>', methods=['POST'])
@login_required
@role_required('admin')
def cambiar_estado_usuario(nombre_usuario):
    # No permitir darse de baja a sí mismo
    if nombre_usuario == session.get('usuario'):
        flash('No puedes darte de baja a ti mismo.', 'danger')
        return redirect(url_for('admin.gestion_bajas'))
    
    estado_actual = request.form.get('estado_actual') == '1'

    if estado_actual:
        exito = UsuarioDAO.delete(nombre_usuario)
        accion = "dado de BAJA"
    else:
        db = Database()
        conn = db.get_connection()
        exito = False
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE Usuarios SET activo = 1 WHERE nombreUsuario = ?", (nombre_usuario,))
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
        flash(f'Error al procesar la solicitud.', 'danger')

    return redirect(url_for('admin.gestion_bajas'))


# --- PERFIL DEL ADMIN (para editar su propia información) ---
@admin_bp.route('/admin/perfil', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def perfil():
    usuario = UsuarioDAO.get_by_nombreUsuario(session.get('usuario'))
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.email = request.form.get('email')
        usuario.dni = request.form.get('dni')
        usuario.fechaNacimiento = request.form.get('fecha_nacimiento') or None
        usuario.telefono = request.form.get('telefono')
        password = request.form.get('password')

        # Validar teléfono en edición
        if usuario.telefono and usuario.telefono.strip():
            if not re.match(r'^\d{9}$', usuario.telefono):
                flash('El teléfono debe tener exactamente 9 dígitos, sin espacios.', 'danger')
                return redirect(url_for('admin.perfil'))

        if password and password.strip():
            usuario.password = password.strip()

        if UsuarioDAO.update(usuario):
            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "UPDATE Usuarios SET telefono = ?, fechaNacimiento = ? WHERE nombreUsuario = ?",
                        (usuario.telefono, usuario.fechaNacimiento, usuario.nombreUsuario)
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error al actualizar perfil: {e}")
                    conn.rollback()
                finally:
                    cursor.close()
            flash('Perfil actualizado correctamente.', 'success')
        else:
            flash('Error al actualizar el perfil.', 'danger')

        return redirect(url_for('admin.perfil'))

    # GET: Cargar datos
    db = Database()
    conn = db.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT fechaNacimiento, telefono FROM Usuarios WHERE nombreUsuario = ?",
                (usuario.nombreUsuario,)
            )
            row = cursor.fetchone()
            if row:
                if row[0]:
                    usuario.fechaNacimiento = row[0]
                if row[1]:
                    usuario.telefono = row[1]
        except Exception as e:
            print(f"Error al cargar datos: {e}")
        finally:
            cursor.close()

    return render_template('admin/perfil.html', usuario=usuario)


# --- PERFIL DEL TRABAJADOR (para editar su propia información) ---
@admin_bp.route('/trabajador/perfil', methods=['GET', 'POST'])
@login_required
@role_required('trabajador')
def perfil_trabajador():
    usuario = UsuarioDAO.get_by_nombreUsuario(session.get('usuario'))
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('auth.dashboard_redirect'))

    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.email = request.form.get('email')
        usuario.dni = request.form.get('dni')
        usuario.fechaNacimiento = request.form.get('fecha_nacimiento') or None
        usuario.telefono = request.form.get('telefono')
        password = request.form.get('password')

        # Validar teléfono en edición
        if usuario.telefono and usuario.telefono.strip():
            if not re.match(r'^\d{9}$', usuario.telefono):
                flash('El teléfono debe tener exactamente 9 dígitos, sin espacios.', 'danger')
                return redirect(url_for('admin.perfil_trabajador'))

        if password and password.strip():
            usuario.password = password.strip()

        if UsuarioDAO.update(usuario):
            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "UPDATE Usuarios SET telefono = ?, fechaNacimiento = ? WHERE nombreUsuario = ?",
                        (usuario.telefono, usuario.fechaNacimiento, usuario.nombreUsuario)
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error al actualizar perfil: {e}")
                    conn.rollback()
                finally:
                    cursor.close()
            flash('Perfil actualizado correctamente.', 'success')
        else:
            flash('Error al actualizar el perfil.', 'danger')

        return redirect(url_for('admin.perfil_trabajador'))

    # GET: Cargar datos
    db = Database()
    conn = db.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT fechaNacimiento, telefono FROM Usuarios WHERE nombreUsuario = ?",
                (usuario.nombreUsuario,)
            )
            row = cursor.fetchone()
            if row:
                if row[0]:
                    usuario.fechaNacimiento = row[0]
                if row[1]:
                    usuario.telefono = row[1]
        except Exception as e:
            print(f"Error al cargar datos: {e}")
        finally:
            cursor.close()

    return render_template('trabajador/perfil.html', usuario=usuario)


# --- CREAR NUEVO ADMIN ---
@admin_bp.route('/admin/crear-admin', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def crear_admin():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo')
        nombre_usuario = request.form.get('nombre_usuario').strip().lower()
        dni = request.form.get('dni')
        email = request.form.get('email')
        password = request.form.get('password')
        telefono = request.form.get('telefono')

        # Validaciones
        if not UsuarioDAO.validar_dni(dni):
            flash('El DNI introducido no es válido.', 'danger')
            return redirect(url_for('admin.crear_admin'))

        if telefono and telefono.strip():
            if not re.match(r'^\d{9}$', telefono):
                flash('El teléfono debe tener exactamente 9 dígitos, sin espacios.', 'danger')
                return redirect(url_for('admin.crear_admin'))

        if UsuarioDAO.get_by_nombreUsuario(nombre_usuario):
            flash(f'El nombre de usuario "{nombre_usuario}" ya está ocupado.', 'warning')
            return redirect(url_for('admin.crear_admin'))

        if UsuarioDAO.get_by_dni(dni):
            flash(f'Ya existe un usuario con el DNI {dni}.', 'danger')
            return redirect(url_for('admin.crear_admin'))

        try:
            nuevo_admin = Usuario(
                nombreUsuario=nombre_usuario,
                Nombre=nombre_completo,
                DNI=dni,
                Rol='admin',
                password=password,
                email=email
            )

            if not UsuarioDAO.create(nuevo_admin):
                flash('Error al crear la cuenta de administrador.', 'danger')
                return redirect(url_for('admin.crear_admin'))

            # Guardar teléfono
            if telefono:
                db = Database()
                conn = db.get_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "UPDATE Usuarios SET telefono = ? WHERE nombreUsuario = ?",
                            (telefono, nombre_usuario)
                        )
                        conn.commit()
                    except Exception as e:
                        print(f"Error al guardar teléfono: {e}")
                    finally:
                        cursor.close()

            # Crear registro en Administrador
            db = Database()
            conn = db.get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO Administrador (nombreUsuario) VALUES (?)",
                        (nombre_usuario,)
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error al crear registro de administrador: {e}")
                    conn.rollback()
                finally:
                    cursor.close()

            flash(f'Administrador {nombre_completo} creado correctamente.', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            flash(f'Error crítico: {str(e)}', 'danger')
            return redirect(url_for('admin.crear_admin'))

    return render_template('admin/crear_admin.html')