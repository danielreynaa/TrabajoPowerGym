# src/Vista/VistaMenuEntrenador.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from src.Vista.VistaSeleccionAtletasAsignados import VistaSeleccionAtletasAsignados
from src.Vista.VistaSeleccionAtletaAsignarEntrenamiento    import VistaSeleccionAtletaAsignarEntrenamiento
from src.Logs.Logger import CustomLogger

class VistaMenuEntrenador(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuEntrenador.ui", self)
        self.usuario = usuario      # SuperVo

        # Logger
        self.logger  = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaMenuEntrenador: cargada para usuario {self.usuario.email} (ID {self.usuario.id_usuario}).")

        # Conexiones
        self.botonVerProgreso.clicked.connect(self.abrir_progreso)
        self.botonAsignarRutina.clicked.connect(self.abrir_rutinas)

    def mostrar(self):
        """Callback para volver a esta ventana."""
        self.logger.info(f"VistaMenuEntrenador: mostrado de nuevo para {self.usuario.email}.")
        self.show()

    def abrir_progreso(self):
        """Navega a la selección de atletas para ver progreso."""
        self.logger.info(f"Navegando a VistaSeleccionAtletasAsignados para {self.usuario.email}.")
        self.ventana_progreso = VistaSeleccionAtletasAsignados(self.usuario, self.mostrar)
        self.ventana_progreso.show()
        self.close()

    def abrir_rutinas(self):
        self.logger.info(f"Navegando a VistaSeleccionAtletaRutina para {self.usuario.email}.")
        self.ventana_rutinas = VistaSeleccionAtletaAsignarEntrenamiento(self.usuario, self.mostrar)
        self.ventana_rutinas.show()
        self.close()