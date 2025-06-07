# VistaHistorial.py
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
from src.Conexion.Conexion import Conexion

class VistaHistorial(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaHistorial.ui", self)

        self.usuario = usuario
        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.cargar_historial()
        self.mostrar_records()

    def obtener_id_usuario(self):
        self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.usuario["email"],))
        return self.cursor.fetchone()[0]

    def cargar_historial(self):
        id_usuario = self.obtener_id_usuario()

        self.cursor.execute("""
            SELECT e.fecha_entrenamiento, r.tipo_levantamiento, r.peso_kg
            FROM Entrenamientos e
            JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
            WHERE e.id_atleta = ?
            ORDER BY e.fecha_entrenamiento DESC
        """, (id_usuario,))
        registros = self.cursor.fetchall()

        self.tablaHistorial.setRowCount(len(registros))
        self.tablaHistorial.setColumnCount(3)
        self.tablaHistorial.setHorizontalHeaderLabels(["Fecha", "Ejercicio", "Peso (kg)"])

        for fila, (fecha, ejercicio, peso) in enumerate(registros):
            self.tablaHistorial.setItem(fila, 0, QTableWidgetItem(str(fecha)))
            self.tablaHistorial.setItem(fila, 1, QTableWidgetItem(ejercicio))
            self.tablaHistorial.setItem(fila, 2, QTableWidgetItem(str(peso)))

    def mostrar_records(self):
        id_usuario = self.obtener_id_usuario()

        ejercicios = {
            "Sentadilla": self.recordSentadilla,
            "Banca": self.recordPressBanca,
            "Peso Muerto": self.recordPesoMuerto
        }

        for ejercicio, label in ejercicios.items():
            self.cursor.execute("""
                SELECT MAX(r.peso_kg)
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
            """, (id_usuario, ejercicio))
            max_peso = self.cursor.fetchone()[0]
            texto = f"{ejercicio}: {max_peso if max_peso else '-'} kg"
            label.setText(texto)