from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton 
from PyQt5 import uic

from src.Modelo.BO.HistorialBO import HistorialBO 

from src.Logs.Logger import CustomLogger

class VistaHistorial(QMainWindow):
    def __init__(self, usuario, volver_callback): 
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaHistorial.ui", self)

        self.usuario = usuario
        self.volver_callback = volver_callback 

        self.historial_bo = HistorialBO() 

        self.logger = CustomLogger() 
        self.logger.info(f"Vista Historial cargada para usuario: {self.usuario.email}.") 

        self.btn_volver.clicked.connect(self.volver_al_menu) 

        self.cargar_historial()
        self.mostrar_records()
        self.mostrar_totales_entrenamiento() 
    
    def cargar_historial(self):
        self.logger.info(f"Cargando historial de entrenamientos para usuario: {self.usuario.email}.") 
        historial_data, mensaje_error = self.historial_bo.obtener_historial_completo_atleta(self.usuario.email) 

        if historial_data is None:
            self.logger.error(f"Fallo al cargar historial para {self.usuario.email}. Mensaje: {mensaje_error}") 
            QMessageBox.critical(self, "Error de Carga", mensaje_error)
            self.tablaHistorial.setRowCount(0)
            return

        self.tablaHistorial.setRowCount(len(historial_data)) 
        self.tablaHistorial.setColumnCount(6) 
        self.tablaHistorial.setHorizontalHeaderLabels(["Fecha", "Ejercicio", "Peso (kg)", "Reps", "Series", "RPE"])
        self.tablaHistorial.resizeColumnsToContents() 

        for fila, registro in enumerate(historial_data):
            self.tablaHistorial.setItem(fila, 0, QTableWidgetItem(str(registro[0]))) 
            self.tablaHistorial.setItem(fila, 1, QTableWidgetItem(str(registro[1]))) 
            self.tablaHistorial.setItem(fila, 2, QTableWidgetItem(str(registro[2]))) 
            self.tablaHistorial.setItem(fila, 3, QTableWidgetItem(str(registro[3]))) 
            self.tablaHistorial.setItem(fila, 4, QTableWidgetItem(str(registro[4]))) 
            self.tablaHistorial.setItem(fila, 5, QTableWidgetItem(str(registro[5] if registro[5] is not None else '-')))

        self.logger.debug(f"Historial cargado con {len(historial_data)} registros para {self.usuario.email}.") 
        
    def mostrar_records(self):
        self.logger.info(f"Mostrando récords de levantamiento para usuario: {self.usuario.email}.") 
        records, mensaje_error = self.historial_bo.obtener_records_atleta(self.usuario.email) 

        if records is None:
            self.logger.error(f"Fallo al cargar récords para {self.usuario.email}. Mensaje: {mensaje_error}")
            QMessageBox.critical(self, "Error de Carga", mensaje_error)
            self.recordSentadilla.setText("Sentadilla: - kg")
            self.recordPressBanca.setText("Banca: - kg")
            self.recordPesoMuerto.setText("Peso Muerto: - kg")
            return

        ejercicios_labels = { 
            "Sentadilla": self.recordSentadilla, 
            "Banca": self.recordPressBanca,
            "Peso Muerto": self.recordPesoMuerto
        }

        for ejercicio, label in ejercicios_labels.items():
            max_peso = records.get(ejercicio, '-') 
            texto = f"{ejercicio}: {max_peso if max_peso is not None else '-'} kg"
            label.setText(texto)
            self.logger.debug(f"Record para {ejercicio}: {texto}") 
    
    def mostrar_totales_entrenamiento(self):
        self.logger.info(f"Mostrando totales de entrenamiento por ejercicio para usuario: {self.usuario.email}.") 
        conteos, mensaje_error = self.historial_bo.obtener_conteo_entrenamientos_por_ejercicio(self.usuario.email) 

        if conteos is None:
            self.logger.error(f"Fallo al cargar conteos de entrenamiento para {self.usuario.email}. Mensaje: {mensaje_error}") 
            QMessageBox.critical(self, "Error de Carga", mensaje_error)
            self.totalSentadilla.setText("Sentadilla Total: -")
            self.totalPressBanca.setText("Banca Total: -")
            self.totalPesoMuerto.setText("Peso Muerto Total: -")
            return

        self.totalSentadilla.setText(f"Sentadilla Total: {conteos.get('Sentadilla', 0)}")
        self.totalPressBanca.setText(f"Press Banca Total: {conteos.get('Banca', 0)}")
        self.totalPesoMuerto.setText(f"Peso Muerto Total: {conteos.get('Peso Muerto', 0)}")
        self.logger.debug(f"Conteos de entrenamiento actualizados: {conteos}.")

    def volver_al_menu(self):
        self.logger.info(f"Volviendo de Vista Historial a Vista Menu Atleta para usuario: {self.usuario.email}.") 
        self.close() 
        if self.volver_callback:
            self.volver_callback()