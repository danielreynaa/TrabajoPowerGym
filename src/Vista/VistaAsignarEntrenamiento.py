# src/Vista/VistaAsignarEntrenamiento.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import hashlib
from src.Logs.Logger import CustomLogger
from src.controlador.ControladorEntrenamiento import ControladorEntrenamiento
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo

class VistaAsignarEntrenamiento(QMainWindow):
    def __init__(self, entrenador_vo, atleta_vo, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaAsignarEntrenamiento.ui", self)

        self.entrenador    = entrenador_vo
        self.atleta        = atleta_vo
        self.volver_cb     = volver_callback

        # Logger
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(
            f"VistaAsignarEntrenamiento: Entrenador={self.entrenador.email} asignando a Atleta={self.atleta.email}"
        )

        # Controlador de entrenamiento
        self.ctrl_entreno = ControladorEntrenamiento()

        # --- POBLAR COMBO DE ATLETAS ---
        # Aquí sólo metemos el atleta seleccionado y deshabilitamos el combo:
        self.comboAtleta.clear()
        display = f"{self.atleta.nombre} {self.atleta.apellidos}"
        self.comboAtleta.addItem(display, self.atleta.id_usuario)
        self.comboAtleta.setEnabled(False)

        # Conectar botones
        self.btn_volver.clicked.connect(self.volver)
        self.botonGuardar.clicked.connect(self.guardar_sesion)

    def guardar_sesion(self):
        """Recoge datos de UI y crea la sesión en BD."""
        id_atleta = self.comboAtleta.currentData()
        id_entrenador = self.entrenador.id_usuario
        fecha = self.fechaEntrenamiento.date().toString("yyyy-MM-dd")

        # Creamos el VO
        vo = EntrenamientoVo(
            id_entrenamiento   = None,
            id_atleta          = id_atleta,
            id_entrenador      = id_entrenador,
            fecha_entrenamiento= fecha,
            notas              = None
        )

        try:
            nuevo_id = self.ctrl_entreno.crear_sesion(vo)
            if nuevo_id:
                self.logger.info(f"Sesión creada ID={nuevo_id} para atleta={id_atleta}.")
                QMessageBox.information(
                    self, 
                    "Éxito", 
                    f"Sesión de entrenamiento creada (ID={nuevo_id})."
                )
                self.volver()
            else:
                raise Exception("ID retornado es None")
        except Exception as e:
            self.logger.error(f"Error al guardar sesión: {e}")
            QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo crear la sesión: {e}"
            )

    def volver(self):
        """Cierra esta ventana y vuelve al menú."""
        self.logger.info("VistaAsignarEntrenamiento: volviendo.")
        self.close()
        if self.volver_cb:
            self.volver_cb()
