# VistaEntrenamiento.py actualizado

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic
from datetime import datetime
from src.Conexion.Conexion import Conexion

class VistaEntrenamiento(QMainWindow):
    def __init__(self, usuario, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamiento.ui", self)

        self.usuario = usuario  # diccionario con al menos 'email'
        self.volver_callback = volver_callback

        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

        # Botón para volver
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setGeometry(10, 10, 120, 30)
        self.btn_volver.clicked.connect(self.volver_al_menu)

    def guardar_entrenamiento(self):
        ejercicios = {
            "Sentadilla": self.pesoSentadilla.text(),
            "Banca": self.pesoPressBanca.text(),
            "Peso Muerto": self.pesoPesoMuerto.text()
        }

        nuevos_maximos = []
        id_usuario = self.obtener_id_usuario()

        # Insertar entrenamiento principal
        fecha_entreno = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO Entrenamientos (id_atleta, fecha_entrenamiento) VALUES (?, ?)",
                            (id_usuario, fecha_entreno))
        id_entrenamiento = self.cursor.lastrowid

        for ejercicio, peso in ejercicios.items():
            try:
                peso_float = float(peso)
            except ValueError:
                continue

            maximo_actual = self.obtener_maximo(id_usuario, ejercicio)
            if peso_float > maximo_actual:
                nuevos_maximos.append(f"{ejercicio}: {peso_float} kg (nuevo récord)")

            self.cursor.execute("""
                INSERT INTO RegistrosLevantamientos (id_entrenamiento, tipo_levantamiento, peso_kg, repeticiones, series, rpe)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_entrenamiento, ejercicio, peso_float, 1, 1, None))

        self.conn.commit()

        if nuevos_maximos:
            QMessageBox.information(self, "¡Nuevos récords!", "\n".join(nuevos_maximos))
        else:
            QMessageBox.information(self, "Guardado", "Entrenamiento registrado correctamente.")

        self.volver_al_menu()

    def obtener_id_usuario(self):
        self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.usuario["email"],))
        return self.cursor.fetchone()[0]

    def obtener_maximo(self, id_usuario, ejercicio):
        self.cursor.execute("""
            SELECT MAX(r.peso_kg)
            FROM Entrenamientos e
            JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
            WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
        """, (id_usuario, ejercicio))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado[0] else 0

    def volver_al_menu(self):
        if self.volver_callback:
            self.close()
            self.volver_callback()
