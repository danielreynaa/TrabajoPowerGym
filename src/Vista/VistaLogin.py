from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.VO.LoginVo import LoginVo
from src.controlador.ControladorUser import ControladorUser
from src.Vista.VistaMenuAtleta import VistaMenuAtleta
from src.Vista.VistaMenuEntrenador import VistaMenuEntrenador
from src.Vista.VistaMenuAdministrador import VistaMenuAdministrador

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = ControladorUser()
        self.botonaceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        email      = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        # Hash SHA-256
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash)

        if self.controller.login(login_vo):
            usuario = self.controller.obtener_usuario_por_email(email)
            if not usuario:
                QMessageBox.critical(self, "Error", "No se pudo obtener datos del usuario.")
                return

            rol = usuario.get("rol", "")
            # Abrir directamente el menú según rol
            if rol == "Atleta":
                self.ventana = VistaMenuAtleta(usuario)
            elif rol == "Entrenador":
                self.ventana = VistaMenuEntrenador(usuario)
            elif rol == "Administrador":
                self.ventana = VistaMenuAdministrador(usuario)
            else:
                QMessageBox.warning(self, "Error", "Rol de usuario no reconocido.")
                return

            self.ventana.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")
