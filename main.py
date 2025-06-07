
from PyQt5.QtWidgets import QApplication
import sys
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from src.Vista.VistaInicial import VistaInicial 
from src.Logs.Logger import CustomLogger 

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    logger_app = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
    logger_app.info("Aplicación PowerGym iniciada.")
    logger_app.debug("Modo de depuración de logs activado.")
   
    ventana_inicial = VistaInicial()
    ventana_inicial.show()
    sys.exit(app.exec_())