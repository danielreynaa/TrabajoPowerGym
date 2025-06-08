# src/Vista/VistaEntrenamientosAsignados.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

from src.Logs.Logger import CustomLogger
from src.controlador.ControladorEntrenamiento import ControladorEntrenamiento

class VistaEntrenamientosAsignados(QMainWindow):
    def __init__(self, entrenador_vo, atleta_vo, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamientosAsignados.ui", self)

        self.entrenador = entrenador_vo
        self.atleta      = atleta_vo
        self.volver_cb   = volver_callback

        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(
            f"VistaEntrenamientosAsignados: cargada para entrenador "
            f"{self.entrenador.email} viendo atleta {self.atleta.email}"
        )

        # Controlador de sesiones
        self.ctrl_entreno = ControladorEntrenamiento()
        # Debes implementar este método en el controlador:
        #   listar_entrenamientos_asignados(id_entrenador, id_atleta)
        sesiones = self.ctrl_entreno.listar_entrenamientos_asignados(
            id_entrenador = self.entrenador.id_usuario,
            id_atleta     = self.atleta.id_usuario
        )

        # Poblar la tabla ordenadas por fecha desc
        self.tblEntrenamientos.setRowCount(len(sesiones))
        for row, sesion in enumerate(sesiones):
            # sesion.fecha_entrenamiento es un datetime.date o str "YYYY-MM-DD"
            fecha = (
                sesion.fecha_entrenamiento
                if isinstance(sesion.fecha_entrenamiento, str)
                else sesion.fecha_entrenamiento.isoformat()
            )
            self.tblEntrenamientos.setItem(row, 0, QTableWidgetItem(fecha))
            self.tblEntrenamientos.setItem(row, 1, QTableWidgetItem(sesion.notas or ""))

        # Conectar botón volver
        self.btn_volver.clicked.connect(self.volver)

    def volver(self):
        self.logger.info("VistaEntrenamientosAsignados: volviendo a selección de atletas.")
        self.close()
        if self.volver_cb:
            self.volver_cb()
