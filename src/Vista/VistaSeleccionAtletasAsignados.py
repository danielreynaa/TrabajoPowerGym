# src/Vista/VistaSeleccionAtletasAsignados.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

from src.controlador.ControladorUser import ControladorUser
from src.Logs.Logger import CustomLogger
from src.Vista.VistaEntrenamientosAsignados import VistaEntrenamientosAsignados

class VistaSeleccionAtletasAsignados(QMainWindow):
    def __init__(self, entrenador_vo, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaSeleccionAtletasAsignados.ui", self)

        self.entrenador     = entrenador_vo
        self.volver_callback = volver_callback

        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaSeleccionAtletasAsignados: cargada para {self.entrenador.email} (ID {self.entrenador.id_usuario}).")

        self.ctrl_user = ControladorUser()
        self.atletas   = self.ctrl_user.listar_usuarios_por_rol("Atleta")
        self.logger.info(f"VistaSeleccionAtletasAsignados: encontrados {len(self.atletas)} atletas.")

        self.tblAtletas.setRowCount(len(self.atletas))
        for row, atleta in enumerate(self.atletas):
            self.tblAtletas.setItem(row, 0, QTableWidgetItem(str(atleta.id_usuario)))
            self.tblAtletas.setItem(row, 1, QTableWidgetItem(atleta.nombre))
            self.tblAtletas.setItem(row, 2, QTableWidgetItem(atleta.apellidos))

        # Ahora reaccionamos al doble‐clic (o un solo clic si prefieres)
        self.tblAtletas.cellDoubleClicked.connect(self.abrir_entrenamientos_asignados)
        self.btn_volver.clicked.connect(self.volver)

    def abrir_entrenamientos_asignados(self, row, _col):
        atleta = self.atletas[row]
        self.logger.info(f"Seleccionado atleta {atleta.email} para ver entrenamientos asignados.")
        # Guarda la ventana en un atributo, ¡muy importante!
        self.ventana_entrenamientos = VistaEntrenamientosAsignados(
            entrenador_vo   = self.entrenador,
            atleta_vo       = atleta,
            volver_callback = self.show
        )
        self.ventana_entrenamientos.show()
        self.close()

    def volver(self):
        self.logger.info("VistaSeleccionAtletasAsignados: volviendo al menú entrenador.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
