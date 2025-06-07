from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.VO.LoginVo import LoginVo
from src.controlador.ControladorUser import ControladorUser
from src.Logs.Logger import CustomLogger
from src.Vista.VistaMenuAtleta import VistaMenuAtleta
from src.Vista.VistaMenuEntrenador import VistaMenuEntrenador
from src.Vista.VistaMenuAdministrador import VistaMenuAdministrador

Form, Window = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self, callback_login_exitoso=None):
        super().__init__()
        self.setupUi(self)

        # Callback opcional para notificar al que llame cuando el login sea exitoso
        self.callback_login_exitoso = callback_login_exitoso

        # Controlador de usuario y logger
        self.controller = ControladorUser()
        self.logger = CustomLogger()
        self.logger.info("Vista Login cargada.")

        # Conectar el botón de login
        self.botonaceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        email = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        # Hashear la contraseña para comparar con la base de datos
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash)

        if self.controller.login(login_vo):
            # Si es correcto, obtenemos el usuario completo para conocer su rol
            usuario = self.controller.obtener_usuario_por_email(email)
            if not usuario:
                QMessageBox.critical(self, "Error", "No se pudo obtener los datos del usuario.")
                return

            rol = usuario.get("rol", "")

            # Abrir la ventana correspondiente según el rol
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

            # Notificar al callback externo si existe
            if self.callback_login_exitoso:
                self.callback_login_exitoso(usuario)

            # Cerrar la ventana de login
            self.close()
        else:
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")
