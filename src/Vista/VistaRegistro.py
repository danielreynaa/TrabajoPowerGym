
from PyQt5.QtWidgets import QMainWindow 
from PyQt5 import uic

Form_Registro, Window_Registro = uic.loadUiType("./src/vista/Ui/VistaRegistro.ui")

class VistaRegistro(QMainWindow, Form_Registro):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
