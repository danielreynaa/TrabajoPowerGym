# src/Vista/VistaMenuEntrenador.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from src.Vista.VistaSeleccionAtletaProgreso import VistaSeleccionAtletaProgreso
from src.Vista.VistaSeleccionAtletaRutina import VistaSeleccionAtletaRutina
from src.Logs.Logger import CustomLogger

class VistaMenuEntrenador(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuEntrenador.ui", self)
        self.usuario = usuario      # SuperVo
        self.logger  = CustomLogger()
        self.logger.info(f"Vista Menu Entrenador cargada para usuario: {self.usuario.email}")

        self.botonVerProgreso.   clicked.connect(self.abrir_progreso)
        self.botonAsignarRutina. clicked.connect(self.abrir_rutinas)

    def mostrar(self):
        self.logger.info(f"Volviendo a VistaMenuEntrenador para usuario: {self.usuario.email}")
        self.show()

    def abrir_progreso(self):
        self.logger.info(f"Navegando a VistaSeleccionAtletaProgreso para {self.usuario.email}")
        # Pasamos usuario y callback
        self.ventana_progreso = VistaSeleccionAtletaProgreso(self.usuario, self.mostrar)
        self.ventana_progreso.show()
        self.close()

    def abrir_rutinas(self):
        self.logger.info(f"Navegando a VistaSeleccionAtletaRutina para {self.usuario.email}")
        self.ventana_rutinas = VistaSeleccionAtletaRutina(self.usuario, self.mostrar)
        self.ventana_rutinas.show()
        self.close()
