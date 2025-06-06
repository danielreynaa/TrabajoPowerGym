from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class VistaMenuEntrenador(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuEntrenador.ui", self)
        self.usuario = usuario