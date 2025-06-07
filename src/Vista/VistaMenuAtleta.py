# src/Vista/VistaMenuAtleta.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from src.Vista.VistaEntrenamiento import VistaEntrenamiento
from src.Vista.VistaHistorial import VistaHistorial
from src.Vista.VistaProgreso import VistaProgreso
from src.Vista.VistaPerfil import VistaPerfil

class VistaMenuAtleta(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAtleta.ui", self)
        self.usuario = usuario  # Este debe ser un diccionario con al menos el campo "email"

        # Conexión de botones
        self.botonEntrenamiento.clicked.connect(self.abrir_entrenamiento)
        self.botonHistorial.clicked.connect(self.abrir_historial)
        self.botonProgreso.clicked.connect(self.abrir_progreso)
        self.botonPerfil.clicked.connect(self.abrir_perfil)

    def mostrar(self):
        self.show()

    def abrir_entrenamiento(self):
        self.ventana_entrenamiento = VistaEntrenamiento(self.usuario, self.mostrar)
        self.ventana_entrenamiento.show()
        self.close()

    def abrir_historial(self):
        self.ventana_historial = VistaHistorial(self.usuario, self.mostrar)
        self.ventana_historial.show()
        self.close()

    def abrir_progreso(self):
        self.ventana_progreso = VistaProgreso(self.usuario, self.mostrar)
        self.ventana_progreso.show()
        self.close()

    def abrir_perfil(self):
        try:
            print("▶ Abriendo VistaPerfil")
            self.ventana_perfil = VistaPerfil(self.usuario["email"], self.mostrar)
            self.ventana_perfil.show()
            self.close()
        except Exception as e:
            print("❌ Error al abrir VistaPerfil:", e)
