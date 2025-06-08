# C:\Users\elded\OneDrive\Escritorio\INGENIERÍA DE SOFTWARE\POWER GYM\TrabajoPowerGym\src\Vista\VistaMenuAtleta.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from src.Vista.VistaEntrenamiento import VistaEntrenamiento
from src.Vista.VistaHistorial import VistaHistorial
# ELIMINADO: from src.Vista.VistaProgreso import VistaProgreso
from src.Vista.VistaPerfil import VistaPerfil

from src.Logs.Logger import CustomLogger

class VistaMenuAtleta(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAtleta.ui", self)
        self.usuario = usuario  

        self.logger = CustomLogger()
        self.logger.info(f"Vista Menu Atleta cargada para usuario: {self.usuario.email}")

        self.botonEntrenamiento.clicked.connect(self.abrir_entrenamiento)
        self.botonHistorial.clicked.connect(self.abrir_historial)
        # ELIMINADO: self.botonProgreso.clicked.connect(self.abrir_progreso)
        self.botonPerfil.clicked.connect(self.abrir_perfil)

    def mostrar(self):
        self.logger.info(f"Volviendo a Vista Menu Atleta para usuario: {self.usuario.email}")
        self.show()

    def abrir_entrenamiento(self):
        self.logger.info(f"Navegando de VistaMenuAtleta a VistaEntrenamiento para usuario: {self.usuario.email}")
        self.ventana_entrenamiento = VistaEntrenamiento(self.usuario, self.mostrar)
        self.ventana_entrenamiento.show()
        self.close()

    def abrir_historial(self):
        self.logger.info(f"Navegando de VistaMenuAtleta a VistaHistorial para usuario: {self.usuario.email}")
        self.ventana_historial = VistaHistorial(self.usuario, self.mostrar)
        self.ventana_historial.show()
        self.close()

    # ELIMINADO: Método abrir_progreso ya no existe
    # def abrir_progreso(self):
    #     self.logger.info(f"Navegando de Vista Menu Atleta a VistaProgreso para usuario: {self.usuario.email}")
    #     self.ventana_progreso = VistaProgreso(self.usuario, self.mostrar)
    #     self.ventana_progreso.show()
    #     self.close()

    def abrir_perfil(self):
        try:
            self.logger.info(f"Navegando de VistaMenuAtleta a VistaPerfil para usuario: {self.usuario.email}")
            self.ventana_perfil = VistaPerfil(self.usuario.email, self.mostrar)
            self.ventana_perfil.show()
            self.close()
        except Exception as e:
            self.logger.error(f"Error al abrir VistaPerfil para usuario {self.usuario.email}: {e}")