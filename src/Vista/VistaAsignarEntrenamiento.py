# src/Vista/VistaAsignarEntrenamiento.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

from src.controlador.ControladorEntrenamiento import ControladorEntrenamiento
from src.controlador.ControladorRegistroLevantamiento import ControladorRegistroLevantamiento
from src.Logs.Logger import CustomLogger

class VistaAsignarEntrenamiento(QMainWindow):
    def __init__(self, entrenador_vo, atleta_vo, volver_callback):
        super().__init__()
        # Carga la UI correcta
        uic.loadUi("src/Vista/Ui/VistaAsignarEntrenamiento.ui", self)

        # ValueObjects y callback
        self.entrenador      = entrenador_vo
        self.atleta          = atleta_vo
        self.volver_callback = volver_callback

        # Controladores y logger
        self.ctrl_sesion   = ControladorEntrenamiento()
        self.ctrl_registro = ControladorRegistroLevantamiento()
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(
            f"VistaAsignarEntrenamiento: Entrenador={self.entrenador.email} "
            f"→ Atleta={self.atleta.email}"
        )

        # Conexiones de botones
        self.btn_volver.clicked.connect(self.volver)
        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

    def guardar_entrenamiento(self):
        """Crea sesión y registra los levantamientos introducidos."""
        try:
            # 1) Crear sesión
            fecha = self.fechaEntrenamiento.date().toString("yyyy-MM-dd")
            id_sesion = self.ctrl_sesion.crear_sesion(
                id_atleta=self.atleta.id_usuario,
                fecha=fecha,
                notas=None
            )
            self.logger.info(f"Sesión creada ID={id_sesion}")

            # 2) Datos de levantamientos
            ejercicios = [
                ("Sentadilla",   self.pesoSentadilla,   self.spinRepeticionesSentadilla,   self.spinSeriesSentadilla,   self.spinRPESentadilla),
                ("Press Banca",  self.pesoPressBanca,   self.spinRepeticionesBanca,        self.spinSeriesBanca,        self.spinRPEBanca),
                ("Peso Muerto",  self.pesoPesoMuerto,   self.spinRepeticionesPesoMuerto,   self.spinSeriesPesoMuerto,   self.spinRPEPesoMuerto),
            ]

            resultados = []
            for tipo, wPeso, wRep, wSer, wRPE in ejercicios:
                peso = float(wPeso.text() or 0)
                reps = wRep.value()
                series = wSer.value()
                rpe = wRPE.value()
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
                    if ok:
                        resultados.append(f"{tipo}: {peso}kg x{series}x{reps}")
                    else:
                        resultados.append(f"{tipo}: fallo al registrar")

            # 3) Mensaje al usuario
            if resultados:
                QMessageBox.information(
                    self,
                    "Entrenamiento Asignado",
                    "Se han registrado:\n" + "\n".join(resultados)
                )
            else:
                QMessageBox.warning(
                    self,
                    "Sin datos",
                    "No introdujiste datos válidos para ningún levantamiento."
                )

            # 4) Volver atrás
            self.volver()

        except Exception as e:
            self.logger.error(f"Error asignando entrenamiento: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")

    def volver(self):
        """Cierra esta ventana y llama al callback de la anterior."""
        self.logger.info("VistaAsignarEntrenamiento: volviendo.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
