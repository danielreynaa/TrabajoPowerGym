from PyQt5.QtWidgets import QMainWindow, QLabel, QDateEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QDate
from src.Conexion.Conexion import Conexion
from datetime import datetime

class VistaAsignarRutina(QMainWindow):
    def __init__(self, atleta, volver_callback):
        super().__init__()
        self.atleta = atleta
        self.volver_callback = volver_callback
        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.setWindowTitle("Asignar Rutina")

        self.lbl_nombre = QLabel(f"Asignar rutina a: {atleta['nombre']} {atleta['apellidos']} ({atleta['email']})")
        self.fecha = QDateEdit(QDate.currentDate())
        self.fecha.setCalendarPopup(True)

        self.sentadilla = QLineEdit()
        self.sentadilla.setPlaceholderText("Sentadilla (kg)")
        self.banca = QLineEdit()
        self.banca.setPlaceholderText("Press Banca (kg)")
        self.peso_muerto = QLineEdit()
        self.peso_muerto.setPlaceholderText("Peso Muerto (kg)")

        self.btn_guardar = QPushButton("Asignar Rutina")
        self.btn_volver = QPushButton("Volver")

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_nombre)
        layout.addWidget(self.fecha)
        layout.addWidget(self.sentadilla)
        layout.addWidget(self.banca)
        layout.addWidget(self.peso_muerto)
        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_volver)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_volver.clicked.connect(self.volver)

    def guardar(self):
        fecha_str = self.fecha.date().toString("yyyy-MM-dd")
        id_usuario = self.obtener_id_usuario()
        self.cursor.execute("INSERT INTO Entrenamientos (id_atleta, fecha_entrenamiento) VALUES (?, ?)",
                            (id_usuario, fecha_str))
        id_entrenamiento = self.cursor.lastrowid

        for ejercicio, campo in {
            "Sentadilla": self.sentadilla,
            "Banca": self.banca,
            "Peso Muerto": self.peso_muerto
        }.items():
            try:
                peso = float(campo.text())
                self.cursor.execute("""INSERT INTO RegistrosLevantamientos
                    (id_entrenamiento, tipo_levantamiento, peso_kg, repeticiones, series, rpe)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (id_entrenamiento, ejercicio, peso, 1, 1, None))
            except ValueError:
                continue

        self.conn.commit()
        QMessageBox.information(self, "Éxito", "Rutina asignada correctamente.")
        self.volver()

    def obtener_id_usuario(self):
        self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.atleta['email'],))
        return self.cursor.fetchone()[0]

    def volver(self):
        self.close()
        self.volver_callback()
