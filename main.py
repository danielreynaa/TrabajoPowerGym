import sys
from PyQt5.QtWidgets import QApplication
from src.Vista.VistaInicial import VistaInicial 


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.Vista.Login import Login

#Ventana main a ejecutar
if __name__ == "__main__":
    app = QApplication(sys.argv) 


    ventana_inicial = VistaInicial()
    ventana_inicial.show()

    sys.exit(app.exec_()) 












    app = QApplication([])
    ventana = Login()
    ventana.show()
    app.exec_()