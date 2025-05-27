# src/Vista/VistaInicial.py
from PyQt5.QtWidgets import QMainWindow 
from PyQt5 import uic
import sys 
from src.Vista.Login import Login
from src.Vista.VistaRegistro import VistaRegistro

Form_Inicial, Window_Inicial = uic.loadUiType("./src/Vista/Ui/VistaInicial.ui")

class VistaInicial(QMainWindow, Form_Inicial):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 


        self.Registrar.clicked.connect(self.mostrar_registro)

        self.YaRegistrado.clicked.connect(self.mostrar_login)

        self.registro_window = None
        self.login_window = None

    def mostrar_registro(self):
        print("Botón 'Registrarme' presionado. Abriendo VistaRegistro...")
        self.registro_window = VistaRegistro() 
        self.registro_window.show()             
        self.close()                            

    def mostrar_login(self):
        print("Botón 'Ya estoy registrado' presionado. Abriendo VistaLogin...")
        self.login_window = Login() 
        self.login_window.show()    
        self.close()               