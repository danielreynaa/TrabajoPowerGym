# VistaPerfil.py actualizado con callback y boton para volver
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic
from src.Conexion import Conexion
from datetime import datetime

class VistaPerfil(QMainWindow):
    def __init__(self, usuario_email, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaPerfil.ui", self)

        self.usuario = usuario_email  # debe ser string
        self.volver_callback = volver_callback
        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.cargar_datos()
        self.pushButton.clicked.connect(self.guardar_cambios)

        # Botón volver
        self.btn_volver = QPushButton("Volver al menú", self)
        self.btn_volver.setGeometry(10, 10, 150, 30)
        self.btn_volver.clicked.connect(self.volver_al_menu)

    def cargar_datos(self):
        self.cursor.execute("""
            SELECT nombre, apellidos, email, contrasena, fecha_nacimiento, telefono, peso_corporal
            FROM Usuarios
            WHERE email = ?
        """, (self.usuario,))
        datos = self.cursor.fetchone()

        if datos:
            self.inputNombre.setText(datos[0])
            self.inputApellidos.setText(datos[1])
            self.inputEmail.setText(datos[2])
            self.inputContrasena.setText(datos[3])

            if datos[4]:
                fecha = datetime.strptime(datos[4], "%Y-%m-%d")
                self.inpuFechaDeNacimiento.setDate(fecha)

            self.inputTelefono.setText(datos[5] if datos[5] else "")
            self.inputPeso.setValue(float(datos[6] or 0))

    def guardar_cambios(self):
        nombre = self.inputNombre.text()
        apellidos = self.inputApellidos.text()
        contrasena = self.inputContrasena.text()
        fecha_nac = self.inpuFechaDeNacimiento.date().toString("yyyy-MM-dd")
        telefono = self.inputTelefono.text()
        peso = self.inputPeso.value()

        self.cursor.execute("""
            UPDATE Usuarios
            SET nombre = ?, apellidos = ?, contrasena = ?, fecha_nacimiento = ?, telefono = ?, peso_corporal = ?
            WHERE email = ?
        """, (nombre, apellidos, contrasena, fecha_nac, telefono, peso, self.usuario))

        self.conn.commit()
        QMessageBox.information(self, "Perfil actualizado", "Los datos han sido guardados correctamente.")

    def volver_al_menu(self):
        if self.volver_callback:
            self.close()
            self.volver_callback()
