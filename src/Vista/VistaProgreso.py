from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox
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

        # BO y Logger
        self.progreso_bo = ProgresoBO()
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaProgreso: inicializada para {self.usuario.email}.")

        # Configurar canvas de Matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QVBoxLayout(self.graficaWidget)
        layout.addWidget(self.canvas)

        # Conexiones
        self.comboEjercicio.currentTextChanged.connect(self.actualizar_grafica)
        self.btn_volver.clicked.connect(self.volver_al_menu)

        # Primera carga de la gráfica
        self.actualizar_grafica()

    def actualizar_grafica(self):
        email = self.usuario.email
        ejercicio = self.comboEjercicio.currentText()
        self.logger.info(f"VistaProgreso: actualizando gráfica de '{ejercicio}' para {email}.")

        fechas, pesos_raw = self.progreso_bo.obtener_datos_para_grafica(email, ejercicio)
        if fechas is None or pesos_raw is None:
            self.logger.error(f"VistaProgreso: error al obtener datos para '{ejercicio}': {pesos_raw}")
            QMessageBox.critical(self, "Error de Gráfica", str(pesos_raw))
            return

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        if fechas and pesos_raw:
            ax.plot(fechas, pesos_raw, marker='o', linestyle='-')
            self.logger.debug(f"VistaProgreso: gráfica de '{ejercicio}' con {len(fechas)} puntos.")
        else:
            self.logger.info(f"VistaProgreso: sin datos para '{ejercicio}' de {email}.")
            ax.text(
                0.5, 0.5,
                "No hay datos disponibles para este ejercicio.",
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=10,
                color='gray'
            )

        ax.set_title(f"Progreso en {ejercicio}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Peso (kg)")
        ax.grid(True)
        self.canvas.figure.autofmt_xdate()
        self.canvas.draw()

    def volver_al_menu(self):
        email = self.usuario.email
        self.logger.info(f"VistaProgreso: regresando al menú para {email}.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
