import sqlite3
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaProgreso(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaProgreso.ui", self)

        self.usuario = usuario
        self.conn = sqlite3.connect("powergym.db")
        self.cursor = self.conn.cursor()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QVBoxLayout(self.graficaWidget)
        layout.addWidget(self.canvas)

        self.comboEjercicio.currentTextChanged.connect(self.actualizar_grafica)
        self.actualizar_grafica()

    def actualizar_grafica(self):
        ejercicio = self.comboEjercicio.currentText()

        self.cursor.execute("""
            SELECT fecha, peso FROM historial
            WHERE usuario = ? AND ejercicio = ?
            ORDER BY fecha ASC
        """, (self.usuario, ejercicio))
        datos = self.cursor.fetchall()

        fechas = [x[0] for x in datos]
        pesos = [x[1] for x in datos]

        ax = self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(fechas, pesos, marker='o', linestyle='-', color='blue')
        ax.set_title(f"Progreso en {ejercicio}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Peso (kg)")
        ax.grid(True)
        self.canvas.draw()
