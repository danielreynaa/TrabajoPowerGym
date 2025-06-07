
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal 
import hashlib

from src.Modelo.BO.UserBO import UserBO
from src.Modelo.VO.LoginVo import LoginVo
from src.Vista.VistaMenu import VistaMenu 

from src.Logs.Logger import CustomLogger 

Form, Window = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    login_exitoso = pyqtSignal() 

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.botonaceptar.clicked.connect(self.on_button_click)
        self.vista_menu_instance = None 

        self.logger = CustomLogger() 
        self.logger.info("Vista Login cargada.") 

    def on_button_click(self):
        email = self.Nombreusuario.text().strip() 
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            self.logger.warning("Intento de login con campos vacíos.")
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash) 

        user_bo = UserBO()
        if user_bo.comprobar_login(login_vo):
            QMessageBox.information(self, "Login Exitoso", "¡Bienvenido!")
            self.logger.info(f"Usuario {email} ha iniciado sesión exitosamente.") 
            self.close()
            self.vista_menu_instance = VistaMenu()
            self.vista_menu_instance.show()
        else:
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")
            self.logger.error(f"Intento de login fallido para usuario: {email}.") 
            self.Contrasena.clear()