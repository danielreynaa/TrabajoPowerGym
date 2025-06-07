from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaInicial.ui")

class VistaInicial(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Botón “Registrarme” abre Registro
        self.Registrar.clicked.connect(self.mostrar_registro)
        # Botón “Ya estoy registrado” abre Login
        self.YaRegistrado.clicked.connect(self.mostrar_login)

    def mostrar_login(self):
        from src.Vista.VistaLogin import Login
        self.login_window = Login()
        self.login_window.show()
        self.close()

    def mostrar_registro(self):
        from src.Vista.VistaRegistro import VistaRegistro
        self.registro_window = VistaRegistro()
        self.registro_window.show()
        self.close()
