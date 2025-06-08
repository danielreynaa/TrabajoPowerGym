# src/Vista/VistaMenuAdministrador.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from src.Vista.VistaTipoUsuarios import VistaTipoUsuarios
from src.Logs.Logger import CustomLogger

class VistaMenuAdministrador(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAdministrador.ui", self)
        self.usuario = usuario
        self.logger  = CustomLogger()
        self.logger.info(f"Vista Menu Administrador cargada para usuario: {self.usuario.email}")

        self.botonVerUsuarios.clicked.connect(self.abrir_tipo_usuarios)

    def mostrar(self):
        self.logger.info(f"Volviendo a VistaMenuAdministrador para usuario: {self.usuario.email}")
        self.show()

    def abrir_tipo_usuarios(self):
        self.logger.info(f"Navegando a VistaTipoUsuarios para {self.usuario.email}")
        # Le pasamos callback de volver a este menú
        self.ventana_tipo = VistaTipoUsuarios(self.usuario, self.mostrar)
        self.ventana_tipo.show()
        self.close()
