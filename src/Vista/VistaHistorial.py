import sqlite3
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

class VistaHistorial(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaHistorial.ui", self)

        self.usuario = "usuario_demo"  # Reemplazar con el usuario logueado real

        # Conectar a la base de datos
        self.conn = sqlite3.connect("powergym.db")
        self.cursor = self.conn.cursor()

        self.cargar_historial()
        self.mostrar_records()

    def cargar_historial(self):
        self.cursor.execute("""
            SELECT fecha, ejercicio, peso
            FROM historial
            WHERE usuario = ?
            ORDER BY fecha DESC
        """, (self.usuario,))
        registros = self.cursor.fetchall()

        self.tablaHistorial.setRowCount(len(registros))
        self.tablaHistorial.setColumnCount(3)
        self.tablaHistorial.setHorizontalHeaderLabels(["Fecha", "Ejercicio", "Peso (kg)"])

        for fila, (fecha, ejercicio, peso) in enumerate(registros):
            self.tablaHistorial.setItem(fila, 0, QTableWidgetItem(fecha))
            self.tablaHistorial.setItem(fila, 1, QTableWidgetItem(ejercicio))
            self.tablaHistorial.setItem(fila, 2, QTableWidgetItem(str(peso)))

    def mostrar_records(self):
        ejercicios = {
            "Sentadilla": self.recordSentadilla,
            "Press Banca": self.recordPressBanca,
            "Peso Muerto": self.recordPesoMuerto
        }

        for ejercicio, label in ejercicios.items():
            self.cursor.execute("""
                SELECT MAX(peso) FROM historial
                WHERE usuario = ? AND ejercicio = ?
            """, (self.usuario, ejercicio))
            max_peso = self.cursor.fetchone()[0]
            texto = f"{ejercicio}: {max_peso if max_peso else '-'} kg"
            label.setText(texto)
