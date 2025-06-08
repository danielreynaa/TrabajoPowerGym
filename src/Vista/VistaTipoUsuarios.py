# src/Vista/VistaTipoUsuarios.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from src.Vista.VistaListaUsuarios import VistaListaUsuarios
from src.Logs.Logger import CustomLogger

class VistaTipoUsuarios(QMainWindow):
    def __init__(self, usuario, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaTipoUsuarios.ui", self)

        # Guardamos el usuario (VO) y el callback para volver
        self.usuario = usuario
        self.volver_callback = volver_callback

        # Logger
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaTipoUsuarios: cargada para {self.usuario.email} (ID {self.usuario.id_usuario}).")

        # Conectamos los botones
        self.botonAtletas.clicked.connect(lambda: self.ver_lista("Atleta"))
        self.botonEntrenadores.clicked.connect(lambda: self.ver_lista("Entrenador"))
        self.botonVolver.clicked.connect(self.volver)

    def ver_lista(self, rol):
        """
        Abre la ventana de listado de usuarios filtrados por rol.
        """
        self.logger.info(f"VistaTipoUsuarios: viendo lista de '{rol}'.")
        # Si VistaListaUsuarios también necesita el VO de usuario, podrías pasarlo:
        # self.ventana_lista = VistaListaUsuarios(self.usuario, rol, self.show)
        self.ventana_lista = VistaListaUsuarios(rol, self.show)
        self.ventana_lista.show()
        self.close()

    def volver(self):
        """
        Cierra esta ventana y llama al callback para regresar al menú anterior.
        """
        self.logger.info(f"VistaTipoUsuarios: volviendo al menú para {self.usuario.email}.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
