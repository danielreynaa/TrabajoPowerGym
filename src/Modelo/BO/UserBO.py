# C:\Users\elded\OneDrive\Escritorio\POWER GYM\TrabajoPowerGym\src\Modelo\BO\UserBO.py

from src.Modelo.DAO.UserDao import UserDao # Ya existe
from src.Modelo.VO.SuperVo import SuperVo # Ya existe
from src.Modelo.VO.LoginVo import LoginVo # Ya existe
from typing import List, Optional

# Importa el Logger
from src.Logs.Logger import CustomLogger # AÑADIDO

class UserBO:
    def __init__(self):
        self.user_dao = UserDao()
        self.logger = CustomLogger() # AÑADIDO: Inicializa el Logger
        self.logger.info("UserBO inicializado.") # AÑADIDO: Log de inicialización

    def registrar_usuario(self, nombre, apellidos, email, contrasena, rol,
                             fecha_nacimiento=None, telefono=None, peso_corporal=None):
        self.logger.info(f"BO: Intentando registrar usuario: {email} con rol: {rol}.") # AÑADIDO
        if not email or "@" not in email:
            self.logger.warning(f"BO: Fallo de validación de email al registrar usuario: {email}.") # AÑADIDO
            raise ValueError("Email no válido.")
        try:
            self.user_dao.insert_user(
                nombre, apellidos, email, contrasena, rol,
                fecha_nacimiento, telefono, peso_corporal
            )
            self.logger.info(f"BO: Usuario {email} registrado con éxito.") # AÑADIDO
        except Exception as e:
            self.logger.error(f"BO: Error al registrar usuario {email}: {e}") # AÑADIDO
            raise

    def listar_usuarios(self) -> List[SuperVo]:
        self.logger.debug("BO: Listando todos los usuarios.") # AÑADIDO
        return self.user_dao.select()

    def comprobar_login(self, login_vo: LoginVo) -> bool:
        self.logger.info(f"BO: Comprobando login para email: {login_vo.email}.") # AÑADIDO
        return self.user_dao.consulta_login(login_vo.email, login_vo.contrasena)

    def obtener_usuario_por_email(self, email: str) -> Optional[SuperVo]:
        data = self.user_dao.obtener_usuario_por_email(email)  # dict o None
        if not data:
            return None
        return SuperVo(
            id_usuario      = data["id_usuario"],
            nombre          = data["nombre"],
            apellidos       = data["apellidos"],
            email           = data["email"],
            contrasena      = data["contrasena"],
            rol             = data["rol"],
            fecha_registro  = data["fecha_registro"],
            fecha_nacimiento= data.get("fecha_nacimiento"),
            telefono        = data.get("telefono"),
            peso_corporal   = data.get("peso_corporal")
    )

    def eliminar_usuario_por_email(self, email: str) -> bool:
        return self.user_dao.eliminar_usuario(email)

    def actualizar_usuario(self, vo: SuperVo):
        """
        Llama al DAO para actualizar el usuario.
        Si falla, lanza excepción para que la vista la maneje.
        """
        success = self.user_dao.update_user(vo)
        if not success:
            raise Exception("No se pudo actualizar el perfil del usuario.")

    def listar_usuarios_por_rol(self, rol: str) -> List[SuperVo]:
        return self.user_dao.listar_por_rol(rol)
