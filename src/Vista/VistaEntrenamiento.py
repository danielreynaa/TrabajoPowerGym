
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic
from datetime import datetime
    
from src.Modelo.BO.EntrenamientoBO import EntrenamientoBO # MODIFICADO
    
from src.Logs.Logger import CustomLogger 

class VistaEntrenamiento(QMainWindow):
    def __init__(self, usuario, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamiento.ui", self)

        self.usuario = usuario
        self.volver_callback = volver_callback

        self.entrenamiento_bo = EntrenamientoBO() # AÑADIDO

        self.logger = CustomLogger()
        self.logger.info(f"Vista Entrenamiento cargada para usuario: {self.usuario.get('email', 'Desconocido')}.")

        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setGeometry(10, 10, 120, 30) 
        self.btn_volver.clicked.connect(self.volver_al_menu)

    def guardar_entrenamiento(self):
        self.logger.info(f"Intentando guardar entrenamiento para usuario: {self.usuario.get('email', 'Desconocido')}.")
            
        ejercicios_data = {
            "Sentadilla": {
                "peso": self.pesoSentadilla.text(),
                "repeticiones": self.spinRepeticionesSentadilla.value(),
                "series": self.spinSeriesSentadilla.value(),
                "rpe": self.spinRPESentadilla.value()
            },
            "Banca": {
                "peso": self.pesoPressBanca.text(),
                "repeticiones": self.spinRepeticionesBanca.value(),
                "series": self.spinSeriesBanca.value(),
                "rpe": self.spinRPEBanca.value()
            },
            "Peso Muerto": {
                "peso": self.pesoPesoMuerto.text(),
                "repeticiones": self.spinRepeticionesPesoMuerto.value(),
                "series": self.spinSeriesPesoMuerto.value(),
                "rpe": self.spinRPEPesoMuerto.value()
            }
        }

        exito, mensaje, nuevos_maximos = self.entrenamiento_bo.registrar_entrenamiento_completo(
            self.usuario.get('email'), 
            ejercicios_data
        )

        if exito:
            self.logger.info(f"Entrenamiento guardado correctamente para {self.usuario.get('email')}. Mensaje: {mensaje}")
            if nuevos_maximos:
                QMessageBox.information(self, "¡Nuevos récords!", "\n".join(nuevos_maximos))
            else:
                QMessageBox.information(self, "Guardado", mensaje)
            self.volver_al_menu()
        else:
            self.logger.error(f"Fallo al guardar entrenamiento para {self.usuario.get('email')}. Mensaje: {mensaje}")
            QMessageBox.critical(self, "Error al Guardar", mensaje)

    def volver_al_menu(self):
        self.logger.info(f"Volviendo de Vista Entrenamiento a Vista Menu Atleta para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.close() 
        if self.volver_callback:
            self.volver_callback()