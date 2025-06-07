from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from src.Logs.Logger import CustomLogger 
from src.Vista.VistaLogin import Login 
from src.Vista.VistaRegistro import VistaRegistro 
from src.Vista.VistaMenuAtleta import VistaMenuAtleta 

Form, _ = uic.loadUiType("./src/Vista/Ui/VistaInicial.ui")

class VistaInicial(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.logger = CustomLogger() 
        self.logger.info("Vista Inicial cargada.") 

        self.Registrar.clicked.connect(self.mostrar_registro)
        self.YaRegistrado.clicked.connect(self.mostrar_login)

        self.registro_window = None
        self.login_window = None

    def mostrar_login(self):
        self.logger.info("Navegando de Vista Inicial a VistaLogin (botón 'Ya estoy registrado').") 
        self.login_window = Login()
        self.login_window.show()
        self.close()

    def mostrar_registro(self):
        self.logger.info("Navegando de Vista Inicial a VistaRegistro (botón 'Registrarme').") 
        self.registro_window = VistaRegistro()
        self.registro_window.show()
        self.close()
