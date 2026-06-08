import os
from PySide6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QTableWidgetItem
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

ui_path = os.path.join(os.path.dirname(__file__), "editar_usuario.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

ROLES_TRABAJADOR = {'auxiliar', 'especialista', 'coordinador'}


class AdminEditarUsuarioVentana(QMainWindow, Ui_MainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        self.showMaximized()

        self.rol_actual = ""
        self.usuario_editado = None

        self._habilitar_campos_comunes(False)

        self._llenar_buscador_usuarios()
        self.cmb_buscador_usuario.currentIndexChanged.connect(self._al_seleccionar_usuario)

        self.btn_anadir_enfermedad.clicked.connect(self._agregar_enfermedad)
        self.btn_anadir_contacto.clicked.connect(self._agregar_fila_contacto)

        self.cmb_tipo_trabajador.currentTextChanged.connect(self._mostrar_subcampos_trabajador)

        self.btn_guardar.clicked.connect(self._procesar_guardado)
        self.btn_cancelar.clicked.connect(self.close)

    # BUSCADOR

    def _llenar_buscador_usuarios(self):
        self.cmb_buscador_usuario.clear()
        self.cmb_buscador_usuario.addItem("--- Seleccione un usuario ---", None)
        for u in self.controlador.listar_todos_usuarios_dict():
            texto = f"{u['nombre']} ({u['tipo'].capitalize()})"
            self.cmb_buscador_usuario.addItem(texto, u['nombreUsuario'])

    def _al_seleccionar_usuario(self, index):
        nombre_usuario = self.cmb_buscador_usuario.itemData(index)
        if nombre_usuario:
            self.usuario_editado = nombre_usuario
            datos = self.controlador.obtener_usuario_dict(nombre_usuario)
            if datos:
                self._cargar_usuario(datos)
        else:
            self.usuario_editado = None
            self._limpiar_formulario()
            self._habilitar_campos_comunes(False)
            self._ocultar_todos_los_roles()

    # VISIBILIDAD

    def _habilitar_campos_comunes(self, habilitado: bool):
        for nombre in ('txt_nombre', 'txt_dni', 'txt_email',
                       'txt_telefono', 'txt_password', 'date_nacimiento'):
            getattr(self, nombre).setEnabled(habilitado)
        self.btn_guardar.setEnabled(habilitado)

    def _ocultar_todos_los_roles(self):
        self.box_rol_paciente.setVisible(False)
        self.box_rol_trabajador.setVisible(False)
        self.box_rol_admin.setVisible(False)

    def _mostrar_seccion_rol(self, rol: str):
        self._ocultar_todos_los_roles()
        if rol == 'paciente':
            self.box_rol_paciente.setVisible(True)
        elif rol == 'trabajador':
            self.box_rol_trabajador.setVisible(True)
        elif rol == 'admin':
            self.box_rol_admin.setVisible(True)

    def _mostrar_subcampos_trabajador(self, tipo: str):
        tipo = tipo.lower()
        es_auxiliar     = tipo == 'auxiliar'
        es_especialista = tipo == 'especialista'

        self.cmb_horario_auxiliar.setVisible(es_auxiliar)
        self.cmb_horario_auxiliar.setEnabled(es_auxiliar)

        self.txt_especialidad.setVisible(es_especialista)
        self.txt_especialidad.setEnabled(es_especialista)
        self.txt_horario_especialista.setVisible(es_especialista)
        self.txt_horario_especialista.setEnabled(es_especialista)

    # CARGA DE DATOS

    def _cargar_usuario(self, datos: dict):
        self.txt_nombre.setText(datos.get('nombre', ''))
        self.txt_dni.setText(datos.get('dni', ''))
        self.txt_email.setText(datos.get('email', ''))
        self.txt_telefono.setText(datos.get('telefono', ''))
        self.txt_password.setText(datos.get('password', ''))
        self.text_Usuario.setText(datos.get('nombreUsuario', ''))

        fecha_str = datos.get('fechaNacimiento', '')
        if fecha_str:
            self.date_nacimiento.setDate(QDate.fromString(str(fecha_str), 'yyyy-MM-dd'))

        tipo_valor = datos.get('tipo', '').lower()

        if tipo_valor in ROLES_TRABAJADOR:
            self.rol_actual = 'trabajador'
            self._cargar_datos_trabajador(datos, tipo_valor)
        elif tipo_valor == 'admin':
            self.rol_actual = 'admin'
        else:
            self.rol_actual = 'paciente'
            self._cargar_datos_paciente(datos)

        self._habilitar_campos_comunes(True)
        self._mostrar_seccion_rol(self.rol_actual)

    def _cargar_datos_paciente(self, datos: dict):
        idx = self.cmb_tipo_paciente.findText(datos.get('tipo_paciente', 'Público').capitalize())
        if idx >= 0:
            self.cmb_tipo_paciente.setCurrentIndex(idx)

        self.lista_enfermedades.clear()
        for enf in datos.get('enfermedades', []):
            self.lista_enfermedades.addItem(QListWidgetItem(str(enf)))

        self.tableWidget.setRowCount(0)
        for c in datos.get('contactos', []):
            self._agregar_fila_contacto(c)

    def _cargar_datos_trabajador(self, datos: dict, tipo_valor: str):
        idx = self.cmb_tipo_trabajador.findText(tipo_valor.capitalize())
        if idx >= 0:
            self.cmb_tipo_trabajador.setCurrentIndex(idx)

        if tipo_valor == 'auxiliar':
            idx_h = self.cmb_horario_auxiliar.findText(datos.get('horario', ''))
            if idx_h >= 0:
                self.cmb_horario_auxiliar.setCurrentIndex(idx_h)
        elif tipo_valor == 'especialista':
            self.txt_especialidad.setText(datos.get('especialidad', ''))
            self.txt_horario_especialista.setText(datos.get('horario', ''))

        self._mostrar_subcampos_trabajador(tipo_valor)

    # ACCIONES DE PACIENTE

    def _agregar_enfermedad(self):
        texto = self.txt_otra_enfermedad.text().strip()
        if texto:
            self.lista_enfermedades.addItem(QListWidgetItem(texto))
            self.txt_otra_enfermedad.clear()

    def _agregar_fila_contacto(self, contacto=None):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        if isinstance(contacto, dict):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(contacto.get('nombre', '')))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(contacto.get('parentesco', '')))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(contacto.get('telefono', '')))

    # LIMPIAR

    def _limpiar_formulario(self):
        for campo in ('txt_nombre', 'txt_dni', 'txt_email', 'txt_telefono',
                      'txt_password', 'txt_especialidad', 'txt_horario_especialista',
                      'txt_otra_enfermedad', 'text_Usuario'):
            getattr(self, campo).clear()
        self.lista_enfermedades.clear()
        self.tableWidget.setRowCount(0)
        self.rol_actual = ""

    # GUARDAR

    def _obtener_datos_formulario(self) -> dict:
        payload = {
            'nombre':           self.txt_nombre.text().strip(),
            'dni':              self.txt_dni.text().strip(),
            'email':            self.txt_email.text().strip(),
            'telefono':         self.txt_telefono.text().strip(),
            'password':         self.txt_password.text().strip(),
            'fecha_nacimiento': self.date_nacimiento.date().toString('yyyy-MM-dd'),
        }

        if self.rol_actual == 'paciente':
            payload['tipo_paciente'] = self.cmb_tipo_paciente.currentText()
            payload['enfermedades'] = [
                self.lista_enfermedades.item(i).text()
                for i in range(self.lista_enfermedades.count())
            ]
            contactos = []
            for row in range(self.tableWidget.rowCount()):
                def celda(col, r=row):
                    item = self.tableWidget.item(r, col)
                    return item.text().strip() if item else ''
                contactos.append({
                    'nombre':     celda(0),
                    'parentesco': celda(1),
                    'telefono':   celda(2),
                })
            payload['contactos'] = contactos

        elif self.rol_actual == 'trabajador':
            tipo_t = self.cmb_tipo_trabajador.currentText().lower()
            payload['tipo_trabajador'] = tipo_t
            if tipo_t == 'auxiliar':
                payload['horario'] = self.cmb_horario_auxiliar.currentText()
            elif tipo_t == 'especialista':
                payload['especialidad']        = self.txt_especialidad.text().strip()
                payload['horario_especialista'] = self.txt_horario_especialista.text().strip()

        return payload

    def _procesar_guardado(self):
        if not self.usuario_editado:
            QMessageBox.warning(self, "Aviso", "No hay ningún usuario seleccionado para editar.")
            return

        payload = self._obtener_datos_formulario()
        exito, msg = self.controlador.actualizar_usuario(self.usuario_editado, payload)

        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)