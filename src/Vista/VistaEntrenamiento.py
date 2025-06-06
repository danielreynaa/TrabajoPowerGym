# src/Vista/VistaEntrenamiento.py

import sqlite3
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from datetime import datetime

class VistaEntrenamiento(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamiento.ui", self)
        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

        self.conn = sqlite3.connect("powergym.db")
        self.cursor = self.conn.cursor()

        self.usuario = usuario  # usuario es un dict con al menos el campo "email"

    def guardar_entrenamiento(self):
        ejercicios = {
            "Sentadilla": self.pesoSentadilla.text(),
            "Press Banca": self.pesoPressBanca.text(),
            "Peso Muerto": self.pesoPesoMuerto.text()
        }

        nuevos_maximos = []

        for ejercicio, peso in ejercicios.items():
            try:
                peso_int = int(peso)
            except ValueError:
                continue  # Si el valor no es numérico, lo salta

            maximo_actual = self.obtener_maximo(ejercicio)

            if peso_int > maximo_actual:
                nuevos_maximos.append(f"{ejercicio}: {peso_int} kg (nuevo récord)")

            # Insertar el nuevo registro en historial
            self.cursor.execute(
                "INSERT INTO historial (usuario, ejercicio, peso, fecha) VALUES (?, ?, ?, ?)",
                (self.usuario["email"], ejercicio, peso_int, datetime.now().strftime("%Y-%m-%d"))
            )

        self.conn.commit()

        if nuevos_maximos:
            QMessageBox.information(self, "¡Nuevos récords!", "\n".join(nuevos_maximos))
        else:
            QMessageBox.information(self, "Guardado", "Entrenamiento registrado correctamente.")

    def obtener_maximo(self, ejercicio):
        self.cursor.execute(
            "SELECT MAX(peso) FROM historial WHERE usuario = ? AND ejercicio = ?",
            (self.usuario["email"], ejercicio)
        )
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0
