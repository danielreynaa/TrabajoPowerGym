# src/Vista/VistaMenuEntrenador.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from src.Vista.VistaSeleccionAtletaProgreso import VistaSeleccionAtletaProgreso
from src.Vista.VistaSeleccionAtletaRutina import VistaSeleccionAtletaRutina

class VistaMenuEntrenador(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuEntrenador.ui", self)
        self.usuario = usuario

        self.botonVerProgreso.clicked.connect(self.abrir_progreso)
        self.botonAsignarRutina.clicked.connect(self.abrir_rutinas)

    def mostrar(self):
        self.show()

    def abrir_progreso(self):
        self.ventana_progreso = VistaSeleccionAtletaProgreso(self.mostrar)
        self.ventana_progreso.show()
        self.close()

    def abrir_rutinas(self):
        self.ventana_rutinas = VistaSeleccionAtletaRutina(self.mostrar)
        self.ventana_rutinas.show()
        self.close()
