from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from datetime import datetime

from src.controlador.ControladorEntrenamiento import ControladorEntrenamiento
from src.controlador.ControladorRegistroLevantamiento import ControladorRegistroLevantamiento
from src.Logs.Logger import CustomLogger

class VistaAsignarEntrenamiento(QMainWindow):
    def __init__(self, entrenador, atleta, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaAsignarEntrenamiento.ui", self)

        # Guardar parámetros
        self.entrenador      = entrenador
        self.atleta          = atleta
        self.volver_callback = volver_callback

        # Controladores y Logger
        self.ctrl_sesion   = ControladorEntrenamiento()
        self.ctrl_registro = ControladorRegistroLevantamiento()
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(
            f"VistaAsignarEntrenamiento: Entrenador={self.entrenador.email} → Atleta={self.atleta.email}"
        )

        # Conectar botones
        self.btn_volver.clicked.connect(self.volver)
        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

    def guardar_entrenamiento(self):
        try:
            # 1) Crear la sesión de entrenamiento
            fecha_str = self.fechaEntrenamiento.date().toString("yyyy-MM-dd")
            id_sesion = self.ctrl_sesion.crear_sesion(
                self.atleta.id_usuario,          # id_atleta (INT)
                self.entrenador.id_usuario,      # id_entrenador (INT)
                fecha_str,                       # fecha (STR "YYYY-MM-DD")
                None                             # notas
            )
            self.logger.info(f"Sesión creada con ID={id_sesion}")

            # 2) Recoger y registrar levantamientos
            ejercicios = [
                ("Sentadilla",  self.pesoSentadilla,  self.spinRepeticionesSentadilla,  self.spinSeriesSentadilla,  self.spinRPESentadilla),
                ("Banca", self.pesoPressBanca,  self.spinRepeticionesBanca,       self.spinSeriesBanca,       self.spinRPEBanca),
                ("Peso Muerto", self.pesoPesoMuerto,  self.spinRepeticionesPesoMuerto,  self.spinSeriesPesoMuerto,  self.spinRPEPesoMuerto),
            ]
            report = []
            for tipo, wPeso, wRep, wSer, wRPE in ejercicios:
                try:
                    peso = float(wPeso.text() or 0)
                except ValueError:
                    continue
                reps   = wRep.value()
                series = wSer.value()
                rpe    = wRPE.value()
                if peso > 0 and reps > 0 and series > 0:
                    ok = self.ctrl_registro.registrar_levantamiento(
                        id_entrenamiento=id_sesion,
                        id_usuario=self.atleta.id_usuario,
                        tipo=tipo,
                        peso_kg=peso,
                        repeticiones=reps,
                        series=series,
                        rpe=float(rpe)
                    )
                    report.append(f"{tipo}: {'OK' if ok else 'FALLÓ'}")

            # 3) Mostrar resultado
            if report:
                QMessageBox.information(self, "Entrenamiento Asignado", "\n".join(report))
            else:
                QMessageBox.warning(self, "Sin datos", "No se registraron levantamientos.")

            # 4) Volver
            self.volver()

        except Exception as e:
            self.logger.error(f"Error asignando entrenamiento: {e}")
            QMessageBox.critical(self, "Error", str(e))

    def volver(self):
        self.logger.info("VistaAsignarEntrenamiento: volviendo.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
