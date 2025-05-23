class ControladorPrincipal():

    def __init__(self, vista, modelo):
        self._vista = vista
        self._modelo = modelo


    def login(self, nombre): 
        if len(nombre) > 3: 
            loginVO = LoginVO(nombre)
            respuestaLogin = self._modelo.comprobarLogin(loginVO)
            print(respuestaLogin)
            self._vista.show()
        else: 
            print("Nombre inválido")

    def mostrarLogin(self):
        self._vista.show()

    def ocultarLogin(self):
        self._vista.hide()

    def eliminarLogin(self):
        self._vista.close()