# src/Modelo/BO/UserBO.py

from src.Modelo.DAO.UserDao import UserDao
from src.Modelo.VO.SuperVo import SuperVo
from src.Modelo.VO.LoginVo import LoginVo  # VO con email y contrasena
from typing import List

class UserBO:
    def __init__(self):
        self.user_dao = UserDao()

    def registrar_usuario(self, nombre, apellidos, email, contrasena, rol,
                          fecha_nacimiento=None, telefono=None, peso_corporal=None):
        # Validación básica
        if not email or "@" not in email:
            raise ValueError("Email no válido.")
        # Insertar (contraseña en texto plano)
        self.user_dao.insert_user(
            nombre, apellidos, email, contrasena, rol,
            fecha_nacimiento, telefono, peso_corporal
        )

    def listar_usuarios(self) -> List[SuperVo]:
        return self.user_dao.select()

    def comprobar_login(self, login_vo: LoginVo) -> bool:
        # Delegar al DAO: compara email + contrasena tal cual
        return self.user_dao.consulta_login(login_vo.email, login_vo.contrasena)
