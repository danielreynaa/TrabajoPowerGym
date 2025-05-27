# src/Vista/VistaInicial.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

Form_Inicial, Window_Inicial = uic.loadUiType("./src/Vista/Ui/VistaInicial.ui")

class VistaInicial(QMainWindow, Form_Inicial):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
