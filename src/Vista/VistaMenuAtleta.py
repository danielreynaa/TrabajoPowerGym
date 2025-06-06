# src/Vista/VistaMenuAtleta.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class VistaMenuAtleta(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAtleta.ui", self)
