from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.BO.UserBO import UserBO
from src.Modelo.VO.LoginVo import LoginVo

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self, callback_login_exitoso=None):
        super().__init__()
        self.setupUi(self)
        self.botonaceptar.clicked.connect(self.on_button_click)
        self.callback_login_exitoso = callback_login_exitoso

    def on_button_click(self):
        email = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash)

        user_bo = UserBO()

        if user_bo.comprobar_login(login_vo):
            usuario = user_bo.obtener_usuario_por_email(email)
            if not usuario:
                QMessageBox.critical(self, "Error", "No se pudo obtener el rol del usuario.")
                return

            rol = usuario.get("rol", "")
            QMessageBox.information(self, "Login Exitoso", f"Bienvenido {rol}.")

            if self.callback_login_exitoso:
                self.callback_login_exitoso(rol)

            self.close()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
