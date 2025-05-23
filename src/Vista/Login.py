from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar el botón a la función
        self.botonaceptar.clicked.connect(self.on_button_click)

    
    def on_button_click(self):
        print("Botón presionado")
        texto_area = self.Contrasena.text() #Obtenet el texto del campo nombre
        print("El texto es: ")
        print(texto_area)


if __name__ == "__main__":
    app = QApplication([])
    ventana = Login()
    ventana.show()
    app.exec_()