from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic

from src.controlador.ControladorRegistroLevantamiento import ControladorRegistroLevantamiento
from src.Logs.Logger import CustomLogger

class VistaEntrenamiento(QMainWindow):
    def __init__(self, usuario, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamiento.ui", self)

        self.usuario = usuario
        self.volver_callback = volver_callback

        # Único controlador necesario por ahora
        self.ctrl_registro = ControladorRegistroLevantamiento()

        # Logger
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info(f"VistaEntrenamiento: cargada para {self.usuario.email} (ID {self.usuario.id_usuario}).")

        # Botón Guardar
        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)
        # Botón Volver
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setGeometry(10, 10, 120, 30)
        self.btn_volver.clicked.connect(self.volver_al_menu)

    def guardar_entrenamiento(self):
        uid = self.usuario.id_usuario
        email = self.usuario.email
        self.logger.info(f"VistaEntrenamiento: guardando levantamientos para {email} (ID {uid}).")

        ejercicios_data = {
            "Sentadilla": {
                "peso":         float(self.pesoSentadilla.text() or 0),
                "repeticiones": self.spinRepeticionesSentadilla.value(),
                "series":       self.spinSeriesSentadilla.value(),
                "rpe":          self.spinRPESentadilla.value()
            },
            "Banca": {
                "peso":         float(self.pesoPressBanca.text() or 0),
                "repeticiones": self.spinRepeticionesBanca.value(),
                "series":       self.spinSeriesBanca.value(),
                "rpe":          self.spinRPEBanca.value()
            },
            "Peso Muerto": {
                "peso":         float(self.pesoPesoMuerto.text() or 0),
                "repeticiones": self.spinRepeticionesPesoMuerto.value(),
                "series":       self.spinSeriesPesoMuerto.value(),
                "rpe":          self.spinRPEPesoMuerto.value()
            }
        }

        errores = []
        for tipo, datos in ejercicios_data.items():
            try:
                ok = self.ctrl_registro.registrar_levantamiento(
                    id_entrenamiento=None,  # por ahora no tenemos sesiones
                    id_usuario=uid,
                    tipo=tipo,
                    peso_kg=datos["peso"],
                    repeticiones=datos["repeticiones"],
                    series=datos["series"],
                    rpe=datos["rpe"]
                )
                if not ok:
                    errores.append(f"{tipo} no se pudo registrar")
            except Exception as e:
                self.logger.error(f"Error al registrar {tipo}: {e}")
                errores.append(f"{tipo}: {e}")

        if errores:
            self.logger.error(f"VistaEntrenamiento: errores al guardar → {errores}")
            QMessageBox.critical(self, "Error al Guardar", "\n".join(errores))
        else:
            self.logger.info(f"VistaEntrenamiento: todos los levantamientos guardados para {email}.")
            QMessageBox.information(self, "Guardado", "Levantamientos registrados correctamente.")

        # Volver al menú
        self.volver_al_menu()

    def volver_al_menu(self):
        self.logger.info(f"VistaEntrenamiento: regresando al menú para {self.usuario.email}.")
        self.close()
        if self.volver_callback:
            self.volver_callback()
