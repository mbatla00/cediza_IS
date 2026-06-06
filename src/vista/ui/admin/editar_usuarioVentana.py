import os
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QCheckBox, QWidget, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QDate

ui_path = os.path.join(os.path.dirname(__file__), "editar_usuario.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class AdminEditarUsuarioVentana(QMainWindow, Ui_MainWindow):
    # AÑADIDO: Recibe el controlador
    def __init__(self, controlador):
        super().__init__()
        self.setupUi(self)
        self.controlador = controlador
        
        # Almacenes para elementos dinámicos
        self.checkboxes_enfermedades = {}
        self.rol_actual = ""
        self.usuario_editado = None # AÑADIDO: Para recordar a quién editamos
        
        # Conectar eventos dinámicos estilo JS
        self.btn_anadir_enfermedad.clicked.connect(self.agregar_enfermedad_dinamica)
        self.btn_anadir_contacto.clicked.connect(lambda: self.crear_fila_contacto("", "", ""))
        self.cmb_tipo_trabajador.currentTextChanged.connect(self.mostrar_subcampos_trabajador)

        # Conectar botones principales de guardar y cancelar
        if hasattr(self, 'btn_guardar'):
            self.btn_guardar.clicked.connect(self.procesar_guardado)
            
        if hasattr(self, 'btn_cancelar'):
            self.btn_cancelar.clicked.connect(self.close)

    # AÑADIDO: Recibe usuario_vo
    def cargar_usuario(self, usuario_vo, usuario: dict, todas_enfermedades: list, paciente_enfermedades: list, contactos: list):
        self.usuario_editado = usuario_vo # Guardamos el objeto
        self.rol_actual = usuario.get("rol", "admin")
        
        # 1. Rellenar datos comunes
        self.txt_nombre.setText(usuario.get("nombre", ""))
        self.txt_email.setText(usuario.get("email", ""))
        self.txt_dni.setText(usuario.get("dni", ""))
        self.txt_telefono.setText(usuario.get("telefono", ""))
        self.txt_password.clear()
        
        if usuario.get("fechaNacimiento"):
            f = datetime.strptime(usuario["fechaNacimiento"], "%Y-%m-%d").date()
            self.date_nacimiento.setDate(QDate(f.year, f.month, f.day))
        
        # 2. Gestionar visibilidad de contenedores según Rol
        self.widget_rol_paciente.setVisible(self.rol_actual == "paciente")
        self.widget_rol_trabajador.setVisible(self.rol_actual == "trabajador")
        self.widget_rol_admin.setVisible(self.rol_actual == "admin")
        
        # 3. Inicializar secciones específicas
        if self.rol_actual == "paciente":
            self.cmb_tipo_paciente.setCurrentText(usuario.get("tipo", "publico").capitalize())
            self.inicializar_enfermedades(todas_enfermedades, paciente_enfermedades)
            self.inicializar_contactos(contactos)
            
        elif self.rol_actual == "trabajador":
            tipo_t = usuario.get("tipo_trabajador", "auxiliar")
            self.cmb_tipo_trabajador.setCurrentText(tipo_t.capitalize())
            
            # Rellenar subcampos
            self.cmb_horario_auxiliar.setCurrentText(usuario.get("horario", ""))
            self.txt_especialidad.setText(usuario.get("especialidad", ""))
            self.txt_horario_especialista.setText(usuario.get("horario", ""))
            self.mostrar_subcampos_trabajador(self.cmb_tipo_trabajador.currentText())

    # --- SECCIÓN PACIENTE: ENFERMEDADES ---
    def inicializar_enfermedades(self, todas: list, seleccionadas: list):
        # Limpiar layout previo si existiera
        for cb in self.checkboxes_enfermedades.values():
            cb.deleteLater()
        self.checkboxes_enfermedades.clear()
        
        # Inyectar las enfermedades del catálogo base
        for enf in todas:
            cb = QCheckBox(enf["nombre"])
            if enf["id"] in seleccionadas:
                cb.setChecked(True)
            self.layout_enfermedades.addWidget(cb)
            self.checkboxes_enfermedades[str(enf["id"])] = cb

    def agregar_enfermedad_dinamica(self):
        """ Equivalente a agregarEnfermedad() en JS """
        nombre = self.txt_otra_enfermedad.text().strip()
        if not nombre: return
        
        cb = QCheckBox(nombre)
        cb.setChecked(True)
        self.layout_enfermedades.addWidget(cb)
        
        # Guardamos la clave con un prefijo "nueva_" idéntico al HTML
        self.checkboxes_enfermedades[f"nueva_{nombre}"] = cb
        self.txt_otra_enfermedad.clear()

    # --- SECCIÓN PACIENTE: CONTACTOS DE EMERGENCIA ---
    def inicializar_contactos(self, contactos: list):
        # Limpiar contenedor de contactos viejo
        while self.widget_contactos_container.layout().count():
            item = self.widget_contactos_container.layout().takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        if contactos:
            for c in contactos:
                self.crear_fila_contacto(c["nombre"], c["relacion"], c["telefono"])
        else:
            self.crear_fila_contacto("", "", "") # Fila vacía por defecto

    def crear_fila_contacto(self, nombre: str, relacion: str, telefono: str):
        """ Crea una fila con inputs y botón eliminar al vuelo """
        fila = QWidget()
        layout_fila = QHBoxLayout(fila)
        layout_fila.setContentsMargins(0, 0, 0, 0)
        
        txt_n = QLineEdit(nombre); txt_n.setPlaceholderText("Nombre")
        txt_r = QLineEdit(relacion); txt_r.setPlaceholderText("Parentesco")
        txt_t = QLineEdit(telefono); txt_t.setPlaceholderText("Teléfono")
        
        btn_del = QPushButton("🗑️")
        btn_del.setStyleSheet("background-color: red; color: white;")
        # Al pulsar, destruimos el contenedor de la fila completa
        btn_del.clicked.connect(fila.deleteLater)
        
        layout_fila.addWidget(txt_n, 4)
        layout_fila.addWidget(txt_r, 4)
        layout_fila.addWidget(txt_t, 3)
        layout_fila.addWidget(btn_del, 1)
        
        # Guardamos referencias en el objeto para leerlas luego
        fila.txt_nombre = txt_n
        fila.txt_relacion = txt_r
        fila.txt_telefono = txt_t
        
        self.widget_contactos_container.layout().addWidget(fila)

    # --- SECCIÓN TRABAJADOR ---
    def mostrar_subcampos_trabajador(self, tipo: str):
        """ Equivalente a mostrarCamposTrabajador() en JS """
        tipo = tipo.lower()
        self.widget_campos_auxiliar.setVisible(tipo == "auxiliar")
        self.widget_campos_especialista.setVisible(tipo == "especialista")

    # --- EXTRACCIÓN DE PAYLOAD ---
    def obtener_datos_formulario(self) -> dict:
        """ Recolecta todo simulando el parseo del REQUEST POST del servidor """
        qdate = self.date_nacimiento.date()
        fecha_str = f"{qdate.year()}-{qdate.month():02d}-{qdate.day():02d}"
        
        payload = {
            "nombre": self.txt_nombre.text().strip(),
            "email": self.txt_email.text().strip(),
            "dni": self.txt_dni.text().strip(),
            "fecha_nacimiento": fecha_str,
            "telefono": self.txt_telefono.text().strip(),
            "rol": self.rol_actual
        }
        
        if self.txt_password.text().strip():
            payload["password"] = self.txt_password.text().strip()
            
        # Parsea según el rol activo
        if self.rol_actual == "paciente":
            payload["tipo"] = self.cmb_tipo_paciente.currentText().lower()
            
            # Extraer IDs de enfermedades marcadas
            payload["enfermedades"] = [id_enf for id_enf, cb in self.checkboxes_enfermedades.items() if cb.isChecked()]
            
            # Extraer contactos dinámicos recorriendo el Layout
            contactos = []
            container_layout = self.widget_contactos_container.layout()
            for i in range(container_layout.count()):
                fila = container_layout.itemAt(i).widget()
                if fila and hasattr(fila, "txt_nombre"):
                    contactos.append({
                        "nombre": fila.txt_nombre.text().strip(),
                        "relacion": fila.txt_relacion.text().strip(),
                        "telefono": self.txt_telefono.text().strip()
                    })
            payload["contactos"] = contactos
            
        elif self.rol_actual == "trabajador":
            tipo_t = self.cmb_tipo_trabajador.currentText().lower()
            payload["tipo_trabajador"] = tipo_t
            if tipo_t == "auxiliar":
                payload["horario"] = self.cmb_horario_auxiliar.currentText()
            elif tipo_t == "especialista":
                payload["especialidad"] = self.txt_especialidad.text().strip()
                payload["horario_especialista"] = self.txt_horario_especialista.text().strip()
                
        return payload

    # AÑADIDO: Lógica de guardado interna que llama al controlador
    def procesar_guardado(self):
        if not self.usuario_editado:
            QMessageBox.warning(self, "Aviso", "No hay ningún usuario seleccionado para editar.")
            return
            
        payload = self.obtener_datos_formulario()
        
        exito, msg = self.controlador.actualizar_usuario(self.usuario_editado, payload)
        
        if exito:
            QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
            self.close() 
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {msg}")