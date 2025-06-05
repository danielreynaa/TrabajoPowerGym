from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5 import uic
import hashlib

from src.Modelo.BO.UserBO import UserBO
from src.Modelo.VO.LoginVo import LoginVo

Form, Window = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.botonaceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # Esta línea ya está extrayendo el texto del QLineEdit 'Nombreusuario'
        # y lo asigna a la variable 'email'. ¡Esto es correcto para tu propósito!
        email = self.Nombreusuario.text().strip() 
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return
        
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        # Aquí se crea el objeto LoginVo pasando el 'email' (que es el texto del campo Nombreusuario)
        login_vo = LoginVo(email=email, contrasena=contrasena_hash) 
        
        user_bo = UserBO()
        # Y aquí, user_bo.comprobar_login() recibirá ese 'email' para la verificación.
        if user_bo.comprobar_login(login_vo):
            QMessageBox.information(self, "Login Exitoso", "¡Bienvenido!")
            self.close()
            # Aquí podrías abrir una ventana específica según el rol (si lo agregas más adelante)
        else:
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")
