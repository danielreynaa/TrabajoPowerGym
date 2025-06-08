from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.VO.LoginVo import LoginVo
from src.controlador.ControladorUser import ControladorUser
from src.Vista.VistaMenuAtleta import VistaMenuAtleta
from src.Vista.VistaMenuEntrenador import VistaMenuEntrenador
from src.Vista.VistaMenuAdministrador import VistaMenuAdministrador
from src.Logs.Logger import CustomLogger 

Form, _ = uic.loadUiType("src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Controlador y logger
        self.controller  = ControladorUser()
        self.logger      = CustomLogger()
        self.logger.info("Vista Login cargada.")

        # Para mantener viva la ventana de menú
        self.menu_window = None

        # Conectar botón
        self.botonaceptar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        email     = self.Nombreusuario.text().strip()
        password  = self.Contrasena.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            self.logger.warning("Intento de login con campos vacíos.")
            return

        # Hash de la contraseña
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        login_vo      = LoginVo(email=email, contrasena=password_hash)

        if not self.controller.login(login_vo):
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")
            self.logger.error(f"Intento de login fallido para usuario: {email}")
            return

        # Login correcto
        self.logger.info(f"Usuario {email} ha iniciado sesión exitosamente.")

        # Obtenemos el VO completo para saber el rol
        usuario = self.controller.obtener_usuario_por_email(email)
        if not usuario:
            QMessageBox.critical(self, "Error", "No se pudo obtener datos del usuario.")
            self.logger.error(f"No se pudieron obtener datos de {email} tras login exitoso.")
            return

        rol = usuario.rol

        # Selección de la ventana de menú
        try:
            if rol == "Atleta":
                self.menu_window = VistaMenuAtleta(usuario)
                self.logger.info(f"Navegando a VistaMenuAtleta para {email}.")
            elif rol == "Entrenador":
                self.menu_window = VistaMenuEntrenador(usuario)
                self.logger.info(f"Navegando a VistaMenuEntrenador para {email}.")
            elif rol == "Administrador":
                self.menu_window = VistaMenuAdministrador(usuario)
                self.logger.info(f"Navegando a VistaMenuAdministrador para {email}.")
            else:
                self.logger.warning(f"Rol desconocido '{rol}' para {email}.")
                QMessageBox.warning(self, "Error", f"Rol '{rol}' desconocido.")
                return

            # Mostramos y cerramos login
            self.menu_window.show()
            self.close()

        except Exception as e:
            self.logger.error(f"Error al abrir la ventana de menú: {e}")
            QMessageBox.critical(self, "Error", "No se pudo cargar la siguiente ventana.")
