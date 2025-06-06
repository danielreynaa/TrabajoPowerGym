# src/Vista/VistaInicial.py

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from src.Vista.VistaRegistro import VistaRegistro
from src.Vista.VistaLogin import Login
from src.Vista.VistaMenuAtleta import VistaMenuAtleta
from src.Vista.VistaMenuEntrenador import VistaMenuEntrenador
from src.Vista.VistaMenuAdministrador import VistaMenuAdministrador

Form_Inicial, _ = uic.loadUiType("src/Vista/Ui/VistaInicial.ui")

class VistaInicial(QMainWindow, Form_Inicial):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Registrar.clicked.connect(self.mostrar_registro)
        self.YaRegistrado.clicked.connect(self.mostrar_login)

        self.registro_window = None
        self.login_window = None

    def mostrar_registro(self):
        self.registro_window = VistaRegistro()
        self.registro_window.show()
        self.close()

    def mostrar_login(self):
        self.login_window = Login(callback_login_exitoso=self.rol_login_exitoso)
        self.login_window.show()
        self.close()

    def rol_login_exitoso(self, rol):
        if rol == "Atleta":
            self.menu_window = VistaMenuAtleta()
        elif rol == "Entrenador":
            self.menu_window = VistaMenuEntrenador()
        elif rol == "Administrador":
            self.menu_window = VistaMenuAdministrador()
        else:
            return

        self.menu_window.show()
