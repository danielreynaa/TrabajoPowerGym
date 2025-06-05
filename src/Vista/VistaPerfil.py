import sqlite3
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

class VistaPerfil(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaPerfil.ui", self)

        self.usuario = usuario  # Se espera que sea el email

        self.conn = sqlite3.connect("powergym.db")
        self.cursor = self.conn.cursor()

        self.cargar_datos()

        self.pushButton.clicked.connect(self.guardar_cambios)

    def cargar_datos(self):
        self.cursor.execute("""
            SELECT nombre, apellidos, email, contrasena, fecha_nacimiento, telefono, peso
            FROM usuarios
            WHERE email = ?
        """, (self.usuario,))
        datos = self.cursor.fetchone()

        if datos:
            self.inputNombre.setText(datos[0])
            self.inputApellidos.setText(datos[1])
            self.inputEmail.setText(datos[2])
            self.inputContrasena.setText(datos[3])
            self.inpuFechaDeNacimiento.setDate(*map(int, datos[4].split('-')))
            self.inputTelefono.setText(datos[5])
            self.inputPeso.setValue(float(datos[6]))

    def guardar_cambios(self):
        nombre = self.inputNombre.text()
        apellidos = self.inputApellidos.text()
        contrasena = self.inputContrasena.text()
        fecha_nac = self.inpuFechaDeNacimiento.date().toString("yyyy-MM-dd")
        telefono = self.inputTelefono.text()
        peso = self.inputPeso.value()

        self.cursor.execute("""
            UPDATE usuarios
            SET nombre = ?, apellidos = ?, contrasena = ?, fecha_nacimiento = ?, telefono = ?, peso = ?
            WHERE email = ?
        """, (nombre, apellidos, contrasena, fecha_nac, telefono, peso, self.usuario))

        self.conn.commit()

        QMessageBox.information(self, "Perfil actualizado", "Los datos han sido guardados correctamente.")
