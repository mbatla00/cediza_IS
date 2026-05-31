import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Qt

# Cargar el archivo .ui del perfil del paciente
ui_path = os.path.join(os.path.dirname(__file__), "ui", "paciente_perfil.ui")
Ui_MainWindow, _ = loadUiType(ui_path)

class PacientePerfilVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def cargar_datos_perfil(self, datos_usuario: dict, lista_familiares: list):
        """
        Rellena los campos del perfil con la información de la base de datos.
        """
        # 1. Rellenar Datos de Cuenta
        self.txt_usuario.setText(datos_usuario.get("nombreUsuario", ""))
        self.txt_email.setText(datos_usuario.get("email", "Sin correo registrado"))
        
        # 2. Rellenar Datos Personales
        self.txt_nombre.setText(datos_usuario.get("nombre", ""))
        self.txt_dni.setText(datos_usuario.get("dni", ""))
        self.txt_nacimiento.setText(datos_usuario.get("fechaNacimiento", "No registrada"))
        
        # 3. Rellenar Información Adicional
        tipo_paciente = "Público" if datos_usuario.get("tipo") == "publico" else "Privado"
        self.txt_tipo.setText(tipo_paciente)
        self.txt_telefono.setText(datos_usuario.get("telefono", "No registrado"))
        self.txt_rol.setText(datos_usuario.get("rol", "").capitalize())
        
        # 4. Renderizar dinámicamente los contactos de emergencia ({% for familiar in familiares %})
        self.limpiar_contactos_emergencia()
        
        if lista_familiares:
            layout_emergencia = self.box_emergencia.layout()
            
            for familiar in lista_familiares:
                # Creamos un pequeño marco contenedor para cada familiar (estilo tarjeta)
                tarjeta_familiar = QFrame()
                tarjeta_familiar.setFrameShape(QFrame.Shape.StyledPanel)
                tarjeta_familiar.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; padding: 5px;")
                layout_tarjeta = QVBoxLayout(tarjeta_familiar)
                
                # Crear las etiquetas de texto
                lbl_nom = QLabel(f"👤 <b>Nombre:</b> {familiar.get('nombre')}")
                lbl_rel = QLabel(f"👥 <b>Relación:</b> {familiar.get('relacion')}")
                lbl_tel = QLabel(f"📞 <b>Teléfono:</b> {familiar.get('telefono', 'Sin teléfono')}")
                
                layout_tarjeta.addWidget(lbl_nom)
                layout_tarjeta.addWidget(lbl_rel)
                layout_tarjeta.addWidget(lbl_tel)
                
                # Añadir la tarjeta al GroupBox de emergencias
                layout_emergencia.addWidget(tarjeta_familiar)
        else:
            # Caso {% else %} del HTML
            lbl_sin_datos = QLabel("ℹ️ No hay contactos de emergencia registrados.")
            lbl_sin_datos.setStyleSheet("color: gray; font-style: italic;")
            self.box_emergencia.layout().addWidget(lbl_sin_datos)

    def limpiar_contactos_emergencia(self):
        """Limpia el layout de emergencias para evitar duplicados si se recarga"""
        layout = self.box_emergencia.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()