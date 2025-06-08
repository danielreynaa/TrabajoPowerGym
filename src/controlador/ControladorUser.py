from src.Modelo.BO.UserBO import UserBO

from src.Modelo.VO.SuperVo import SuperVo

from typing import List

class ControladorUser:
    def __init__(self):
        self.user_bo = UserBO()

    def login(self, login_vo):
        return self.user_bo.comprobar_login(login_vo)

    def obtener_usuario_por_email(self, email):
        return self.user_bo.obtener_usuario_por_email(email)
    
    def actualizar_usuario(self, vo: SuperVo) -> None:
        return self.user_bo.actualizar_usuario(vo)
        
    def listar_usuarios_por_rol(self, rol: str) -> List[SuperVo]:
        return self.user_bo.listar_usuarios_por_rol(rol)
    