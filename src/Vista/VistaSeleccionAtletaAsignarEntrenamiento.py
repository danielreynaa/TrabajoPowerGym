from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

from src.controlador.ControladorUser import ControladorUser
from src.Logs.Logger import CustomLogger
from src.Vista.VistaAsignarEntrenamiento import VistaAsignarEntrenamiento

class VistaSeleccionAtletaAsignarEntrenamiento(QMainWindow):
    def __init__(self, entrenador, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaSeleccionAtletaAsignarEntrenamiento.ui", self)

        # Guardamos el VO de entrenador y el callback
        self.entrenador      = entrenador
        self.volver_callback = volver_callback

        # Logger
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaSeleccionAtletaAsignarEntrenamiento cargada para {self.entrenador.email}")

        # Controlador de usuarios y carga de atletas
        self.ctrl_user = ControladorUser()
        self.atletas   = self.ctrl_user.listar_usuarios_por_rol("Atleta")
        self.logger.info(f"Encontrados {len(self.atletas)} atletas")

        # Rellenar la tabla
        self.tblAtletas.setRowCount(len(self.atletas))
        for i, atleta in enumerate(self.atletas):
            self.tblAtletas.setItem(i, 0, QTableWidgetItem(str(atleta.id_usuario)))
            self.tblAtletas.setItem(i, 1, QTableWidgetItem(atleta.nombre))
            self.tblAtletas.setItem(i, 2, QTableWidgetItem(atleta.apellidos))

        # Conectar doble‐click y volver
        self.tblAtletas.cellDoubleClicked.connect(self.abrir_asignar_entrenamiento)
        self.btn_volver.clicked.connect(self.volver)

    def abrir_asignar_entrenamiento(self, row, _col):
        atleta = self.atletas[row]
        self.logger.info(f"Seleccionado atleta {atleta.email} para asignar entrenamiento")
        # Llamamos por posición (entrenador, atleta, callback)
        self.ventana_asignar = VistaAsignarEntrenamiento(
            self.entrenador,
            atleta,
            self.show
        )
        self.ventana_asignar.show()
        self.close()

    def volver(self):
        self.logger.info("Volviendo al menú del entrenador")
        self.close()
        if self.volver_callback:
            self.volver_callback()
