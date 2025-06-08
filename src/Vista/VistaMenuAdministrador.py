# src/Vista/VistaMenuAdministrador.py
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from src.Vista.VistaTipoUsuarios import VistaTipoUsuarios

class VistaMenuAdministrador(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAdministrador.ui", self)
        self.usuario = usuario

        self.botonVerUsuarios.clicked.connect(self.abrir_tipo_usuarios)

    def abrir_tipo_usuarios(self):
        self.ventana_tipo = VistaTipoUsuarios(self.show)
        self.ventana_tipo.show()
        self.close()
