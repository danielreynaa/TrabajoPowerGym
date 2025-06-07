from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.BO.UserBO import UserBO
from src.Modelo.VO.LoginVo import LoginVo
from src.controlador.ControladorUser import ControladorUser

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self, callback_login_exitoso=None):
        super().__init__()
        self.setupUi(self)
        self.botonaceptar.clicked.connect(self.on_button_click)
        self.callback_login_exitoso = callback_login_exitoso
        self.controller= ControladorUser()

    def on_button_click(self):
        email = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash)

        if self.controller.login(login_vo):
            usuario = self.controller.obtener_usuario_por_email(email)
            if not usuario:
                QMessageBox.critical(self, "Error", "No se pudo obtener el rol del usuario.")
                return

            rol = usuario.get("rol", "")
            QMessageBox.information(self, "Login Exitoso", f"Bienvenido {rol}.")

            if self.callback_login_exitoso:
                self.callback_login_exitoso(usuario)  # CAMBIO: ahora se pasa el dict completo

            self.close()