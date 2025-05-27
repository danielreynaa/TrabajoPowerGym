# src/Vista/VistaRegistro.py
from PyQt5.QtWidgets import QMainWindow # O PyQt6.QtWidgets
from PyQt5 import uic

# Cargar la interfaz generada desde el archivo .ui para VistaRegistro
# Asegúrate de que la ruta al .ui es correcta desde la ubicación de este archivo.
Form_Registro, Window_Registro = uic.loadUiType("./src/Vista/Ui/VistaRegistro.ui")

class VistaRegistro(QMainWindow, Form_Registro):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets de VistaRegistro

        # Puedes conectar botones aquí si VistaRegistro tiene botones para volver o confirmar
        # Por ejemplo, si tienes un botón para volver al inicio o al login
        # self.btn_volver.clicked.connect(self.volver_a_inicio)
        # self.btn_confirmar_registro.clicked.connect(self.procesar_registro)

    # Puedes añadir métodos para la lógica de registro aquí
    # def procesar_registro(self):
    #    # Lógica para guardar el nuevo usuario en la base de datos
    #    print("Procesando registro...")

    # def volver_a_inicio(self):
    #    from src.Vista.VistaInicial import VistaInicial # Importa aquí si lo necesitas
    #    self.initial_window = VistaInicial()
    #    self.initial_window.show()
    #    self.close()