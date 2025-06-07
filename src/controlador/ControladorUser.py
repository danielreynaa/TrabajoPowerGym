from src.Modelo.BO.UserBO import UserBO

class ControladorUser:
    def __init__(self):
        self.user_bo = UserBO()

    def login(self, login_vo):
        return self.user_bo.comprobar_login(login_vo)

    def obtener_usuario_por_email(self, email):
        return self.user_bo.obtener_usuario_por_email(email)
