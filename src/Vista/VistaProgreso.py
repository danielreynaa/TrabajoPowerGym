
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QPushButton 
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.Modelo.BO.ProgresoBO import ProgresoBO 

from src.Logs.Logger import CustomLogger 

class VistaProgreso(QMainWindow):
    def __init__(self, usuario, volver_callback): 
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaProgreso.ui", self) 

        self.usuario = usuario
        self.volver_callback = volver_callback 

        self.progreso_bo = ProgresoBO() 

        self.logger = CustomLogger() 
        self.logger.info(f"Vista Progreso cargada para usuario: {self.usuario.get('email', 'Desconocido')}.") 

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QVBoxLayout(self.graficaWidget) 
        layout.addWidget(self.canvas)

        self.comboEjercicio.currentTextChanged.connect(self.actualizar_grafica) 
        self.actualizar_grafica() 

        self.btn_volver.clicked.connect(self.volver_al_menu) 
        
    def actualizar_grafica(self):
        self.logger.info(f"Actualizando gráfica para usuario {self.usuario.get('email', 'Desconocido')}.")
        ejercicio = self.comboEjercicio.currentText()
        
        fechas, pesos_raw = self.progreso_bo.obtener_datos_para_grafica(self.usuario.get('email'), ejercicio)

        if fechas is None or pesos_raw is None:
            QMessageBox.critical(self, "Error de Gráfica", pesos_raw) 
            self.logger.error(f"Fallo al obtener datos para gráfica de {ejercicio}.")
            return

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        if fechas and pesos_raw: 
            ax.plot(fechas, pesos_raw, marker='o', linestyle='-', color='blue') 
            self.logger.debug(f"Gráfica de {ejercicio} actualizada con {len(fechas)} puntos de datos.") 
        else:
            self.logger.info(f"No hay datos para {ejercicio} para el usuario {self.usuario.get('email', 'Desconocido')}.")
            ax.text(0.5, 0.5, "No hay datos disponibles para este ejercicio.", 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, fontsize=10, color='gray') 

        ax.set_title(f"Progreso en {ejercicio}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Peso (kg)")
        ax.grid(True)
        self.canvas.figure.autofmt_xdate() 
        self.canvas.draw()
        
    def volver_al_menu(self):
        self.logger.info(f"Volviendo de Vista Progreso a Vista Menu Atleta para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.close() 
        if self.volver_callback:
            self.volver_callback()