
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from src.Vista.VistaEntrenamiento import VistaEntrenamiento
from src.Vista.VistaHistorial import VistaHistorial
from src.Vista.VistaProgreso import VistaProgreso # Ya está importado
from src.Vista.VistaPerfil import VistaPerfil # Ya está importado

from src.Logs.Logger import CustomLogger 

class VistaMenuAtleta(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaMenuAtleta.ui", self)
        self.usuario = usuario  

        self.logger = CustomLogger() 
        self.logger.info(f"Vista Menu Atleta cargada para usuario: {self.usuario.get('email', 'Desconocido')}.") 

        self.botonEntrenamiento.clicked.connect(self.abrir_entrenamiento)
        self.botonHistorial.clicked.connect(self.abrir_historial)
        self.botonProgreso.clicked.connect(self.abrir_progreso)
        self.botonPerfil.clicked.connect(self.abrir_perfil)

    def mostrar(self):
        self.logger.info(f"Volviendo a Vista Menu Atleta para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.show()

    def abrir_entrenamiento(self):
        self.logger.info(f"Navegando de Vista Menu Atleta a VistaEntrenamiento para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.ventana_entrenamiento = VistaEntrenamiento(self.usuario, self.mostrar)
        self.ventana_entrenamiento.show()
        self.close()

    def abrir_historial(self):
        self.logger.info(f"Navegando de Vista Menu Atleta a VistaHistorial para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.ventana_historial = VistaHistorial(self.usuario, self.mostrar)
        self.ventana_historial.show()
        self.close()

    def abrir_progreso(self):
        self.logger.info(f"Navegando de Vista Menu Atleta a VistaProgreso para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        # MODIFICAR: Pasar self.mostrar como callback
        self.ventana_progreso = VistaProgreso(self.usuario, self.mostrar) # MODIFICADO
        self.ventana_progreso.show()
        self.close()

    def abrir_perfil(self):
        try:
            self.logger.info(f"Navegando de Vista Menu Atleta a VistaPerfil para usuario: {self.usuario.get('email', 'Desconocido')}.") 
            # MODIFICAR: Pasar self.mostrar como callback
            self.ventana_perfil = VistaPerfil(self.usuario["email"], self.mostrar) # MODIFICADO
            self.ventana_perfil.show()
            self.close()
        except Exception as e:
            self.logger.error(f"Error al abrir VistaPerfil para usuario {self.usuario.get('email', 'Desconocido')}: {e}")