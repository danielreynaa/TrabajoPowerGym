
from src.Conexion.Conexion import Conexion
from src.Modelo.VO.SuperVo import SuperVo
from typing import List, Optional

from src.Logs.Logger import CustomLogger # AÑADIDO

class UserDao(Conexion): 
    SQL_SELECT = """
        SELECT id_usuario, nombre, apellidos, email, contrasena, rol,
               fecha_registro, fecha_nacimiento, telefono, peso_corporal
        FROM Usuarios
    """
    SQL_INSERT = """
        INSERT INTO Usuarios (
            nombre, apellidos, email, contrasena, rol,
            fecha_nacimiento, telefono, peso_corporal
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    SQL_CONSULTA_LOGIN = """
        SELECT COUNT(*) FROM Usuarios WHERE email = ? AND contrasena = ?
    """
    SQL_SELECT_POR_EMAIL = """
        SELECT id_usuario, nombre, apellidos, email, contrasena, rol,
               fecha_registro, fecha_nacimiento, telefono, peso_corporal
        FROM Usuarios WHERE email = ?
    """

    def __init__(self):
        super().__init__() # Llama al constructor de Conexion
        self.logger = CustomLogger() # AÑADIDO: Inicializa el Logger
        self.logger.info("UserDao inicializado.") # AÑADIDO: Log de inicialización

    def select(self) -> List[SuperVo]:
        cursor = self.getCursor()
        usuarios: List[SuperVo] = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                usuarios.append(SuperVo(*row))
        except Exception as e:
            self.logger.error(f"Error en SELECT de Usuarios: {e}") # AÑADIDO: Usa el logger
        finally:
            cursor.close()
        return usuarios

    def insert_user(self, nombre, apellidos, email, contrasena, rol,
                     fecha_nacimiento=None, telefono=None, peso_corporal=None):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (
                nombre, apellidos, email, contrasena, rol,
                fecha_nacimiento, telefono, peso_corporal
            ))
            self.logger.info(f"Usuario {email} insertado correctamente en BD.") # AÑADIDO: Usa el logger
        except Exception as e:
            self.logger.error(f"Error al insertar usuario {email}: {e}") # AÑADIDO: Usa el logger
        finally:
            cursor.close()

    def consulta_login(self, email: str, contrasena: str) -> bool:
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CONSULTA_LOGIN, (email, contrasena))
            count = cursor.fetchone()[0]
            self.logger.debug(f"Consulta login para {email}. Coincidencias: {count}") # AÑADIDO: Log
            return count == 1
        except Exception as e:
            self.logger.error(f"Error en consulta de login para {email}: {e}") # AÑADIDO: Usa el logger
            return False
        finally:
            cursor.close()

    def obtener_usuario_por_email(self, email: str) -> Optional[dict]:
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_SELECT_POR_EMAIL, (email,))
            fila = cursor.fetchone()
            if fila:
                columnas = [desc[0] for desc in cursor.description]
                self.logger.debug(f"Usuario {email} encontrado por email.") # AÑADIDO: Log
                return dict(zip(columnas, fila))
            self.logger.warning(f"Usuario {email} no encontrado por email.") # AÑADIDO: Log
            return None
        except Exception as e:
            self.logger.error(f"Error al obtener usuario por email {email}: {e}") # AÑADIDO: Usa el logger
            return None
        finally:
            cursor.close()

    def eliminar_usuario(self, email: str) -> bool:
        cursor = self.getCursor()
        try:
            cursor.execute("DELETE FROM Usuarios WHERE email = ?", (email,))
            self.conexion.commit()  # 🔥 IMPORTANTE: Forzar commit manual
            return True
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
            return False
        finally:
            cursor.close()
