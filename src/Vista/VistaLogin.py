
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5 import uic
import hashlib

from src.Modelo.VO.LoginVo import LoginVo
from src.controlador.ControladorUser import ControladorUser
from src.Vista.VistaMenuAtleta import VistaMenuAtleta
from src.Vista.VistaMenuEntrenador import VistaMenuEntrenador
from src.Vista.VistaMenuAdministrador import VistaMenuAdministrador

from src.Logs.Logger import CustomLogger 

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = ControladorUser()
        self.botonaceptar.clicked.connect(self.on_button_click)

        self.logger = CustomLogger() 
        self.logger.info("Vista Login cargada.") 

    def on_button_click(self):
        email        = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()

        if not email or not contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            self.logger.warning("Intento de login con campos vacíos.") 
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        login_vo = LoginVo(email=email, contrasena=contrasena_hash)

        if self.controller.login(login_vo):
            self.logger.info(f"Usuario {email} ha iniciado sesión exitosamente.") 
            
            usuario = self.controller.obtener_usuario_por_email(email)
            if not usuario:
                self.logger.error(f"No se pudieron obtener datos del usuario para {email} después de un login exitoso.") 
                QMessageBox.critical(self, "Error", "No se pudo obtener datos del usuario.")
                return

            rol = usuario.get("rol", "")
            
            if rol == "Atleta":
                self.logger.info(f"Login exitoso para {email} (Rol: Atleta). Navegando a VistaMenuAtleta.")
                self.ventana = VistaMenuAtleta(usuario)
            elif rol == "Entrenador":
                self.logger.info(f"Login exitoso para {email} (Rol: Entrenador). Navegando a VistaMenuEntrenador.")
                self.ventana = VistaMenuEntrenador(usuario)
            elif rol == "Administrador":
                self.logger.info(f"Login exitoso para {email} (Rol: Administrador). Navegando a VistaMenuAdministrador.")
                self.ventana = VistaMenuAdministrador(usuario)
            else:
                self.logger.warning(f"Login exitoso para {email}, pero rol '{rol}' no reconocido. No se pudo navegar.")
                QMessageBox.warning(self, "Error", "Rol de usuario no reconocido.")
                return

            self.ventana.show()
            self.close()
        else:
            self.logger.error(f"Intento de login fallido para usuario: {email}. Credenciales incorrectas.") 
            QMessageBox.critical(self, "Error de Login", "Usuario o contraseña incorrectos.")