from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class VistaMenuAdministrador(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAdministrador.ui", self)
        self.usuario = usuario