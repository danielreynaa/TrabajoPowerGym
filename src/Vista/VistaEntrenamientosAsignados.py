# src/Vista/VistaEntrenamientosAsignados.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic

from src.Logs.Logger import CustomLogger
from src.controlador.ControladorRegistroLevantamiento import ControladorRegistroLevantamiento
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
        self.ctrl_registro = ControladorRegistroLevantamiento()
        self.ctrl_entreno = ControladorEntrenamiento()

        # Obtener las sesiones asignadas
        sesiones = self.ctrl_entreno.listar_entrenamientos_asignados(
            id_entrenador = self.entrenador.id_usuario,
            id_atleta     = self.atleta.id_usuario
        )

        # Configurar tabla: Fecha | Movimientos | Series | Repeticiones | RPE | Notas
        self.tblEntrenamientos.setColumnCount(6)
        self.tblEntrenamientos.setHorizontalHeaderLabels([
            "Fecha", "Movimientos", "Series", "Repeticiones", "RPE", "Notas"
        ])

        self.tblEntrenamientos.setRowCount(len(sesiones))
        for row, sesion in enumerate(sesiones):
            # Fecha
            fecha = (
                sesion.fecha_entrenamiento
                if isinstance(sesion.fecha_entrenamiento, str)
                else sesion.fecha_entrenamiento.isoformat()
            )
            self.tblEntrenamientos.setItem(row, 0, QTableWidgetItem(fecha))

            # Aquí va el cambio: llamamos al método correcto
            detalles = self.ctrl_registro.listar_movimientos_por_sesion(
                id_sesion = sesion.id_entrenamiento
            )

            movimientos  = ", ".join(d.tipo_levantamiento        for d in detalles)
            series       = ", ".join(str(d.series)      for d in detalles)
            repeticiones = ", ".join(str(d.repeticiones)for d in detalles)
            rpes         = ", ".join(str(d.rpe)         for d in detalles)

            self.tblEntrenamientos.setItem(row, 1, QTableWidgetItem(movimientos))
            self.tblEntrenamientos.setItem(row, 2, QTableWidgetItem(series))
            self.tblEntrenamientos.setItem(row, 3, QTableWidgetItem(repeticiones))
            self.tblEntrenamientos.setItem(row, 4, QTableWidgetItem(rpes))

            # Notas al final
            self.tblEntrenamientos.setItem(row, 5, QTableWidgetItem(sesion.notas or ""))

        # Conectar botón volver
        self.btn_volver.clicked.connect(self.volver)

    def volver(self):
        self.logger.info("VistaEntrenamientosAsignados: volviendo a selección de atletas.")
        self.close()
        if self.volver_cb:
            self.volver_cb()
