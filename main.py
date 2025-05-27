import sys
from PyQt5.QtWidgets import QApplication
from src.Vista.VistaInicial import VistaInicial 


if __name__ == "__main__":
    app = QApplication(sys.argv) 


    ventana_inicial = VistaInicial()
    ventana_inicial.show()

    sys.exit(app.exec_()) 











