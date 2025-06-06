from PyQt5.QtWidgets import QApplication
import sys
from Vista.VistaLogin import Login
from src.Vista.Principal import VistaPrincipal

class ControladorAplicacion:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ventana_login = Login()
        self.ventana_login.botonaceptar.clicked.connect(self.validar_login)
        self.ventana_login.show()

    def validar_login(self):
        # Aquí se valida el login
        usuario = self.ventana_login.Nombreusuario.text()
        contrasena = self.ventana_login.Contrasena.text()

        if usuario == "admin" and contrasena == "1234":  # Login simulado
            print("Login exitoso. Abriendo VistaPrincipal...")
            self.ventana_login.close()
            self.ventana_principal = VistaPrincipal()
            self.ventana_principal.show()
        else:
            print("Credenciales incorrectas")

    def ejecutar(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = ControladorAplicacion()
    app.ejecutar()
