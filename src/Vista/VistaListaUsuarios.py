# src/Vista/VistaListaUsuarios.py
from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from src.Modelo.BO.UserBO import UserBO

class VistaListaUsuarios(QMainWindow):
    def __init__(self, rol, volver_callback):
        super().__init__()
        self.rol = rol
        self.volver_callback = volver_callback
        self.setWindowTitle(f"Usuarios - {rol}s")

        self.lista = QListWidget()
        self.btn_eliminar = QPushButton("Eliminar Usuario")
        self.btn_volver = QPushButton("Volver")

        layout = QVBoxLayout()
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.btn_volver)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        self.btn_volver.clicked.connect(self.volver)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.todos = [u for u in UserBO().listar_usuarios() if u.rol == self.rol]
        self.lista.clear()
        for user in self.todos:
            self.lista.addItem(f"{user.nombre} {user.apellidos} - {user.email}")

    def eliminar_usuario(self):
        item = self.lista.currentItem()
        if not item:
            QMessageBox.warning(self, "Atención", "Seleccione un usuario primero.")
            return

        email = item.text().split("-")[-1].strip()

        # Paso 1: Confirmación
        confirmado = QMessageBox.question(
            self,
            "Confirmación",
            f"¿Deseas eliminar a {email}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmado != QMessageBox.Yes:
            return

        # Paso 2: Preguntar razón de eliminación
        razon, ok = QInputDialog.getText(
            self,
            "Razón de eliminación",
            "¿Por qué estás eliminando a este usuario?"
        )

        if not ok or not razon.strip():
            QMessageBox.information(self, "Cancelado", "Operación cancelada. No se eliminó el usuario.")
            return

        # Paso 3: Eliminar usuario
        exito = UserBO().eliminar_usuario_por_email(email)

        if exito:
            print(f"🗑️ Usuario eliminado: {email}. Razón: {razon}")
            QMessageBox.information(self, "Éxito", f"Usuario eliminado: {email}")
            self.cargar_usuarios()  # Recarga la lista al instante
        else:
            QMessageBox.critical(self, "Error", "No se pudo eliminar el usuario.")


    def volver(self):
        self.close()
        self.volver_callback()
