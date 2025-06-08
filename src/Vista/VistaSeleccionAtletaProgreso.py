from PyQt5.QtWidgets import QMainWindow, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget
from src.Modelo.BO.UserBO import UserBO
from src.Vista.VistaProgreso import VistaProgreso

class VistaSeleccionAtletaProgreso(QMainWindow):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setWindowTitle("Seleccionar Atleta - Ver Progreso")

        self.lista = QListWidget(self)
        self.buscador = QLineEdit(self)
        self.buscador.setPlaceholderText("Buscar atleta por nombre...")

        self.btn_volver = QPushButton("Volver al menú", self)

        layout = QVBoxLayout()
        layout.addWidget(self.buscador)
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_volver)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        self.buscador.textChanged.connect(self.filtrar_lista)
        self.lista.itemDoubleClicked.connect(self.abrir_progreso_atleta)
        self.btn_volver.clicked.connect(self.volver)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.todos = [u for u in UserBO().listar_usuarios() if u.rol == "Atleta"]
        self.actualizar_lista(self.todos)

    def actualizar_lista(self, lista):
        self.lista.clear()
        for user in lista:
            self.lista.addItem(f"{user.nombre} {user.apellidos} - {user.email}")

    def filtrar_lista(self, texto):
        texto = texto.lower()
        filtrados = [u for u in self.todos if texto in u.nombre.lower() or texto in u.apellidos.lower()]
        self.actualizar_lista(filtrados)

    def abrir_progreso_atleta(self, item):
        email = item.text().split("-")[-1].strip()
        atleta = UserBO().obtener_usuario_por_email(email)
        from src.Vista.VistaProgreso import VistaProgreso
        self.progreso = VistaProgreso(atleta, self.show)
        self.progreso.show()
        self.close()

    def volver(self):
        self.close()
        self.volver_callback()
