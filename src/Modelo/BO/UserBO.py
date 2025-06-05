from src.Modelo.DAO.UserDao import UserDao
from src.Modelo.VO.SuperVo import SuperVo
from src.Modelo.VO.LoginVo import LoginVo
from typing import List, Optional

class UserBO:
    def __init__(self):
        self.user_dao = UserDao()

    def registrar_usuario(self, nombre, apellidos, email, contrasena, rol,
                          fecha_nacimiento=None, telefono=None, peso_corporal=None):
        if not email or "@" not in email:
            raise ValueError("Email no válido.")
        self.user_dao.insert_user(
            nombre, apellidos, email, contrasena, rol,
            fecha_nacimiento, telefono, peso_corporal
        )

    def listar_usuarios(self) -> List[SuperVo]:
        return self.user_dao.select()

    def comprobar_login(self, login_vo: LoginVo) -> bool:
        return self.user_dao.consulta_login(login_vo.email, login_vo.contrasena)

    def obtener_usuario_por_email(self, email: str) -> Optional[dict]:
        return self.user_dao.obtener_usuario_por_email(email)
