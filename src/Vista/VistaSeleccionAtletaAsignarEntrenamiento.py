from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

from src.controlador.ControladorUser import ControladorUser
from src.Logs.Logger import CustomLogger
# 1) Importa la nueva vista:
from src.Vista.VistaAsignarEntrenamiento import VistaAsignarEntrenamiento

class VistaSeleccionAtletaAsignarEntrenamiento(QMainWindow):
    def __init__(self, entrenador_vo, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaSeleccionAtletaAsignarEntrenamiento.ui", self)

        self.entrenador      = entrenador_vo
        self.volver_callback = volver_callback

        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"Cargando selección de atletas para asignar entrenamiento por {self.entrenador.email}")

        # Carga los atletas
        self.ctrl_user = ControladorUser()
        self.atletas   = self.ctrl_user.listar_usuarios_por_rol("Atleta")

        self.tblAtletas.setRowCount(len(self.atletas))
        for row, atleta in enumerate(self.atletas):
            self.tblAtletas.setItem(row, 0, QTableWidgetItem(str(atleta.id_usuario)))
            self.tblAtletas.setItem(row, 1, QTableWidgetItem(atleta.nombre))
            self.tblAtletas.setItem(row, 2, QTableWidgetItem(atleta.apellidos))

        # 2) Conecta el doble‐clic al método que abre la asignación
        self.tblAtletas.cellDoubleClicked.connect(self.abrir_asignar_entrenamiento)
        self.btn_volver.clicked.connect(self.volver)

    def abrir_asignar_entrenamiento(self, row, _col):
        atleta = self.atletas[row]
        self.logger.info(f"Seleccionado atleta {atleta.email} para asignar entrenamiento.")
        # 3) Guarda la ventana en un atributo de self
        self.ventana_asignar = VistaAsignarEntrenamiento(
            entrenador_vo   = self.entrenador,
            atleta_vo       = atleta,
            volver_callback = self.show
        )
        self.ventana_asignar.show()
        self.close()

    def volver(self):
        self.logger.info("Volviendo al menú del entrenador.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
