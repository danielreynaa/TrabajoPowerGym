from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox # Importamos QMessageBox para mensajes
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/Vista/Ui/VistaLogin.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  


        self.botonaceptar.clicked.connect(self.on_button_click)


    def on_button_click(self):
        """
        clic del botón de login.
        """
        nombre_usuario = self.Nombreusuario.text().strip()
        contrasena = self.Contrasena.text()             

        print(f"Intento de inicio de sesión:")
        print(f"  Usuario: '{nombre_usuario}'")
        print(f"  Contraseña: '{contrasena}'")


        if not nombre_usuario or not contrasena:
            QMessageBox.warning(self, "Error de Inicio de Sesión", "Por favor, ingrese usuario y contraseña.")
            return


        if nombre_usuario == "admin" and contrasena == "adminpass":
            QMessageBox.information(self, "Inicio de Sesión Exitoso", "¡Bienvenido, Administrador!")

            self.close()
        elif nombre_usuario == "atleta" and contrasena == "atletapass":
             QMessageBox.information(self, "Inicio de Sesión Exitoso", "¡Bienvenido, Atleta!")
             self.close()
        elif nombre_usuario == "entrenador" and contrasena == "entrenadorpass":
             QMessageBox.information(self, "Inicio de Sesión Exitoso", "¡Bienvenido, Entrenador!")
             self.close()
        else:
            QMessageBox.critical(self, "Error de Inicio de Sesión", "Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    app = QApplication([])
    ventana = Login()
    ventana.show()
    app.exec_()