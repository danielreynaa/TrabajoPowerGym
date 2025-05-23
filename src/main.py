from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.Vista.Login import Login

if __name__ == "__main__":
    app = QApplication([])
    ventana = Login()
    ventana.show()
    app.exec_()

















