# src/Vista/VistaTipoUsuarios.py
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from src.Vista.VistaListaUsuarios import VistaListaUsuarios

class VistaTipoUsuarios(QMainWindow):
    def __init__(self, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaTipoUsuarios.ui", self)
        self.volver_callback = volver_callback

        self.botonAtletas.clicked.connect(lambda: self.ver_lista("Atleta"))
        self.botonEntrenadores.clicked.connect(lambda: self.ver_lista("Entrenador"))
        self.botonVolver.clicked.connect(self.volver)

    def ver_lista(self, rol):
        from src.Vista.VistaListaUsuarios import VistaListaUsuarios
        self.ventana_lista = VistaListaUsuarios(rol, self.show)
        self.ventana_lista.show()
        self.close()

    def volver(self):
        self.close()
        self.volver_callback()
