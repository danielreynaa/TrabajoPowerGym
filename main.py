import sys
from PyQt5.QtWidgets import QApplication
from src.Vista.VistaInicial import VistaInicial 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.Vista.VistaLogin import Login
from src.Modelo.BO.UserBO import UserBO
from src.Modelo.VO.LoginVo import LoginVo

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