# C:\Users\elded\OneDrive\Escritorio\INGENIERÍA DE SOFTWARE\POWER GYM\TrabajoPowerGym\src\Vista\VistaProgreso.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QPushButton 
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.Conexion.Conexion import Conexion

from src.Logs.Logger import CustomLogger 

class VistaProgreso(QMainWindow):
    def __init__(self, usuario, volver_callback): 
        super().__init__()
        uic.loadUi("src/Vista/Ui/VistaProgreso.ui", self) # Carga el archivo .ui

        print("DEBUG_FLOW_PROGRESO: Constructor de VistaProgreso ejecutado.") # DEPURACIÓN

        self.usuario = usuario
        self.volver_callback = volver_callback 
        self.conn = Conexion().conexion
        self.cursor = self.conn.cursor()

        self.logger = CustomLogger() 
        self.logger.info(f"Vista Progreso cargada para usuario: {self.usuario.get('email', 'Desconocido')}.") 

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout = QVBoxLayout(self.graficaWidget) 
        layout.addWidget(self.canvas)

        self.comboEjercicio.currentTextChanged.connect(self.actualizar_grafica) 
        self.actualizar_grafica() 

        # Conexión del botón "Volver"
        self.btn_volver.clicked.connect(self.volver_al_menu) 
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print("DEBUG_FLOW_PROGRESO: Botón 'btn_volver' conectado.") # DEPURACIÓN
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def obtener_id_usuario(self):
        self.logger.debug(f"Obteniendo ID de usuario para: {self.usuario.get('email', 'Desconocido')}.")
        try: 
            self.cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (self.usuario["email"],))
            result = self.cursor.fetchone()
            if result:
                self.logger.debug(f"ID de usuario {result[0]} obtenido.")
                return result[0]
            else:
                self.logger.warning(f"No se encontró id_usuario para email: {self.usuario['email']}.")
                QMessageBox.warning(self, "Advertencia", "No se encontró el ID de usuario.")
                return None
        except Exception as e:
            self.logger.error(f"Error al obtener id_usuario para {self.usuario['email']}: {e}")
            QMessageBox.critical(self, "Error de BD", f"Fallo al obtener ID de usuario: {e}")
            return None

    def actualizar_grafica(self):
        self.logger.info(f"Actualizando gráfica para usuario {self.usuario.get('email', 'Desconocido')}.")
        ejercicio = self.comboEjercicio.currentText()
        id_usuario = self.obtener_id_usuario()

        if id_usuario is None:
            self.logger.warning("No se puede actualizar la gráfica sin ID de usuario.")
            QMessageBox.warning(self, "Advertencia", "No se puede cargar el progreso sin el ID del usuario.")
            return

        try: 
            self.cursor.execute("""
                SELECT e.fecha_entrenamiento, r.peso_kg
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
                ORDER BY e.fecha_entrenamiento ASC
            """, (id_usuario, ejercicio))
            datos = self.cursor.fetchall()

            fechas = [str(x[0]) for x in datos] 
            pesos = [float(x[1]) for x in datos]

            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            
            if fechas and pesos:
                ax.plot(fechas, pesos, marker='o', linestyle='-', color='blue')
                self.logger.debug(f"Gráfica de {ejercicio} actualizada con {len(datos)} puntos de datos.")
            else:
                self.logger.info(f"No hay datos para {ejercicio} para el usuario {self.usuario.get('email', 'Desconocido')}.")
                ax.text(0.5, 0.5, "No hay datos disponibles para este ejercicio.", 
                        horizontalalignment='center', verticalalignment='center', 
                        transform=ax.transAxes, fontsize=10, color='gray') 

            ax.set_title(f"Progreso en {ejercicio}")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Peso (kg)")
            ax.grid(True)
            self.canvas.figure.autofmt_xdate() 
            self.canvas.draw()
        except Exception as e:
            self.logger.error(f"Error al actualizar gráfica de progreso para {self.usuario.get('email', 'Desconocido')}, ejercicio {ejercicio}: {e}")
            QMessageBox.critical(self, "Error de Gráfica", f"Fallo al cargar datos para gráfica: {e}")
        
    def volver_al_menu(self):
        print("DEBUG_FLOW_PROGRESO: Método volver_al_menu ejecutado.") # DEPURACIÓN
        self.logger.info(f"Volviendo de Vista Progreso a Vista Menu Atleta para usuario: {self.usuario.get('email', 'Desconocido')}.") # Log de navegación
        self.close() 
        if self.volver_callback:
            print("DEBUG_FLOW_PROGRESO: Llamando a volver_callback().") # DEPURACIÓN
            self.volver_callback()