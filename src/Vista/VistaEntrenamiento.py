# C:\Users\elded\OneDrive\Escritorio\INGENIERÍA DE SOFTWARE\POWER GYM\TrabajoPowerGym\src\Vista\VistaEntrenamiento.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5 import uic
from datetime import datetime
from src.Conexion.Conexion import Conexion

from src.Logs.Logger import CustomLogger 

class VistaEntrenamiento(QMainWindow):
    def __init__(self, usuario, volver_callback):
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaEntrenamiento.ui", self)

        self.usuario = usuario
        self.volver_callback = volver_callback

        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.logger = CustomLogger()
        self.logger.info(f"Vista Entrenamiento cargada para usuario: {self.usuario.get('email', 'Desconocido')}.")

        self.botonGuardar.clicked.connect(self.guardar_entrenamiento)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setGeometry(10, 10, 120, 30) 
        self.btn_volver.clicked.connect(self.volver_al_menu)

    def guardar_entrenamiento(self):
        self.logger.info(f"Intentando guardar entrenamiento para usuario: {self.usuario.get('email', 'Desconocido')}.")
        
        # OBTENER LOS DATOS DE LOS NUEVOS CAMPOS (AHORA DE QSpinBox)
        ejercicios_data = {
            "Sentadilla": {
                "peso": self.pesoSentadilla.text(),
                "repeticiones": self.spinRepeticionesSentadilla.value(), 
                "series": self.spinSeriesSentadilla.value(),             
                "rpe": self.spinRPESentadilla.value()                   # Será un entero (1-10)
            },
            "Banca": {
                "peso": self.pesoPressBanca.text(),
                "repeticiones": self.spinRepeticionesBanca.value(),
                "series": self.spinSeriesBanca.value(),
                "rpe": self.spinRPEBanca.value()
            },
            "Peso Muerto": {
                "peso": self.pesoPesoMuerto.text(),
                "repeticiones": self.spinRepeticionesPesoMuerto.value(),
                "series": self.spinSeriesPesoMuerto.value(),
                "rpe": self.spinRPEPesoMuerto.value()
            }
        }

        nuevos_maximos = []
        id_usuario = self.obtener_id_usuario()

        if id_usuario is None:
            self.logger.warning("No se puede guardar entrenamiento sin ID de usuario.")
            QMessageBox.warning(self, "Advertencia", "No se puede guardar el entrenamiento sin el ID del usuario.")
            return

        try:
            fecha_entreno = datetime.now().strftime("%Y-%m-%d")
            
            self.cursor.execute("INSERT INTO Entrenamientos (id_atleta, fecha_entrenamiento) VALUES (?, ?)",
                                 (id_usuario, fecha_entreno))
            
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            result = self.cursor.fetchone()
            id_entrenamiento = result[0] if result else None
            
            if id_entrenamiento is None:
                raise ValueError("No se pudo obtener el ID del entrenamiento recién insertado.")

            self.logger.debug(f"Entrenamiento {id_entrenamiento} creado para atleta {id_usuario}.")

            for ejercicio, data in ejercicios_data.items():
                peso = data["peso"]
                repeticiones = data["repeticiones"]
                series = data["series"]
                rpe = data["rpe"]

                try:
                    peso_float = float(peso)
                except ValueError:
                    self.logger.warning(f"Peso '{peso}' para {ejercicio} no es un número válido. Se omitirá.")
                    continue 

                maximo_actual = self.obtener_maximo(id_usuario, ejercicio)
                if peso_float > maximo_actual:
                    nuevos_maximos.append(f"{ejercicio}: {peso_float} kg (nuevo récord)")
                    self.logger.info(f"¡Nuevo récord personal para {ejercicio}: {peso_float} kg!")

                # --- MODIFICACIÓN CLAVE: RPE ahora es entero (1-10) ---
                # rpe si es 0 (no se permite por el UI, pero como precaución), lo guardamos como NULL si la columna lo permite
                self.cursor.execute("""
                    INSERT INTO RegistrosLevantamientos (id_entrenamiento, tipo_levantamiento, peso_kg, repeticiones, series, rpe)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_entrenamiento, ejercicio, peso_float, repeticiones, series, rpe if rpe >= 1 and rpe <= 10 else None)) 
                self.logger.debug(f"Registro de levantamiento: Entrenamiento ID {id_entrenamiento}, Ejercicio {ejercicio}, Peso {peso_float}kg, Reps {repeticiones}, Series {series}, RPE {rpe}.")
                # --- FIN MODIFICACIÓN ---

            if nuevos_maximos:
                self.logger.info(f"Entrenamiento guardado con nuevos récords: {', '.join(nuevos_maximos)}")
                QMessageBox.information(self, "¡Nuevos récords!", "\n".join(nuevos_maximos))
            else:
                self.logger.info("Entrenamiento guardado sin nuevos récords.")
                QMessageBox.information(self, "Guardado", "Entrenamiento registrado correctamente.")

            self.volver_al_menu()

        except Exception as e:
            self.logger.error(f"Error al guardar entrenamiento para usuario {self.usuario.get('email', 'Desconocido')}: {e}") 
            QMessageBox.critical(self, "Error", f"Fallo al guardar entrenamiento: {e}")

    def obtener_id_usuario(self):
        self.logger.debug(f"Obteniendo ID de usuario para email: {self.usuario.get('email', 'Desconocido')}.")
        try:
            self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.usuario["email"],))
            resultado = self.cursor.fetchone()
            
            if resultado: 
                id_atleta = resultado[0]
                self.logger.debug(f"ID de usuario encontrado: {id_atleta}.")
                return id_atleta
            else:
                self.logger.warning(f"No se encontró ID de usuario en la BD para email: {self.usuario['email']}.")
                QMessageBox.warning(self, "Advertencia", "No se encontró el ID de usuario para la sesión actual.")
                return None
        except Exception as e:
            self.logger.error(f"Error en obtener_id_usuario para {self.usuario.get('email', 'Desconocido')}: {e}")
            QMessageBox.critical(self, "Error de BD", f"Fallo al obtener ID de usuario: {e}")
            return None

    def obtener_maximo(self, id_usuario, ejercicio):
        self.logger.debug(f"Obteniendo máximo para {ejercicio}, usuario ID: {id_usuario}.")
        try:
            self.cursor.execute("""
                SELECT MAX(r.peso_kg)
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
            """, (id_usuario, ejercicio))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado[0] else 0
        except Exception as e:
            self.logger.error(f"Error al obtener máximo de {ejercicio} para usuario {id_usuario}: {e}")
            return 0

    def volver_al_menu(self):
        self.logger.info(f"Volviendo de Vista Entrenamiento a Vista Menu Atleta para usuario: {self.usuario.get('email', 'Desconocido')}.") 
        self.close() 
        if self.volver_callback:
            self.volver_callback()