from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.Conexion.Conexion import Conexion

class VistaProgreso(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaProgreso.ui", self)

        self.usuario = usuario
        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QVBoxLayout(self.graficaWidget)
        layout.addWidget(self.canvas)

        self.comboEjercicio.currentTextChanged.connect(self.actualizar_grafica)
        self.actualizar_grafica()

    def obtener_id_usuario(self):
        self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.usuario["email"],))
        return self.cursor.fetchone()[0]

    def actualizar_grafica(self):
        ejercicio = self.comboEjercicio.currentText()
        id_usuario = self.obtener_id_usuario()

        self.cursor.execute("""
            SELECT e.fecha_entrenamiento, r.peso_kg
            FROM Entrenamientos e
            JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
            WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
            ORDER BY e.fecha_entrenamiento ASC
        """, (id_usuario, ejercicio))
        datos = self.cursor.fetchall()

        fechas = [x[0] for x in datos]
        pesos = [float(x[1]) for x in datos]

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(fechas, pesos, marker='o', linestyle='-', color='blue')
        ax.set_title(f"Progreso en {ejercicio}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Peso (kg)")
        ax.grid(True)
        self.canvas.draw()