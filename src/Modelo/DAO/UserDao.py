from src.Conexion.Conexion import Conexion
from src.Modelo.VO.SuperVo import SuperVo
from typing import List, Optional

from src.Logs.Logger import CustomLogger 

class UserDao(Conexion): 
    SQL_SELECT = """
        SELECT id_usuario, nombre, apellidos, email, contrasena, rol,
               fecha_registro, fecha_nacimiento, telefono, peso_corporal
        FROM Usuarios
    """
    SQL_INSERT = """
        INSERT INTO Usuarios (
            nombre, apellidos, email, contrasena, rol,
            fecha_nacimiento, telefono, peso_ corporal
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

    SQL_UPDATE = """
        UPDATE Usuarios
        SET nombre = ?,
            apellidos = ?,
            contrasena = ?,
            fecha_nacimiento = ?,
            telefono = ?,
            peso_corporal = ?
        WHERE email = ?
    """
    SQL_DELETE = """
        DELETE FROM Usuarios WHERE email = ?
    """ 

    def __init__(self):
        super().__init__() 

        self.cursor = self.getCursor() 

        self.logger = CustomLogger() 
        self.logger.info("UserDao inicializado.") 

    def select(self) -> List[SuperVo]:
        cursor = self.getCursor() 
        usuarios: List[SuperVo] = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                usuarios.append(SuperVo(*row))
        except Exception as e:
            self.logger.error(f"Error en SELECT de Usuarios: {e}") 
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
            self.logger.info(f"Usuario {email} insertado correctamente en BD.") 
        except Exception as e:
            self.logger.error(f"Error al insertar usuario {email}: {e}") 
            raise 
        finally:
            cursor.close()

    def consulta_login(self, email: str, contrasena: str) -> bool:
        cursor = self.getCursor() 
        try:
            cursor.execute(self.SQL_CONSULTA_LOGIN, (email, contrasena))
            count = cursor.fetchone()[0]
            self.logger.debug(f"Consulta login para {email}. Coincidencias: {count}") 
            return count == 1
        except Exception as e:
            self.logger.error(f"Error en consulta de login para {email}: {e}") 
            return False
        finally:
            cursor.close()

    def obtener_id_por_email(self, email: str) -> Optional[int]:
        cursor = self.getCursor() 
        try:
            self.logger.debug(f"DAO: Buscando ID de usuario para email: {email}.")
            cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = ?", (email,))
            resultado = cursor.fetchone()
            if resultado:
                self.logger.debug(f"DAO: ID de usuario {resultado[0]} encontrado para {email}.")
                return resultado[0]
            else:
                self.logger.warning(f"DAO: No se encontró ID de usuario para email: {email}.")
                return None
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener ID de usuario por email {email}: {e}")
            raise 
        finally:
            cursor.close()

    def obtener_usuario_por_email(self, email: str) -> Optional[dict]:
        cursor = self.getCursor() 
        try:
            cursor.execute(self.SQL_SELECT_POR_EMAIL, (email,))
            fila = cursor.fetchone()
            if fila:
                columnas = [desc[0] for desc in cursor.description]
                self.logger.debug(f"Usuario {email} encontrado por email.") 
                return dict(zip(columnas, fila))
            self.logger.warning(f"Usuario {email} no encontrado por email.") 
            return None
        except Exception as e:
            self.logger.error(f"Error al obtener usuario por email {email}: {e}") 
            return None
        finally:
            cursor.close()

    def eliminar_usuario(self, email: str) -> bool: 
        cursor = self.getCursor() 
        try:
<<<<<<< HEAD
            self.logger.info(f"Intentando eliminar usuario: {email}.")
            cursor.execute(self.SQL_DELETE, (email,)) 
            self.logger.info(f"Usuario {email} eliminado correctamente.")
=======
            cursor.execute("DELETE FROM Usuarios WHERE email = ?", (email,))
>>>>>>> 441ccaac75bb8769064dfe5418e4d400450e4ec2
            return True
        except Exception as e:
            self.logger.error(f"Error al eliminar usuario {email}: {e}")
            raise 
        finally:
            cursor.close()

    def update_user(self, vo: SuperVo) -> bool: 
        cursor = self.getCursor() 
        try:
            self.logger.info(f"Actualizando usuario: {vo.email}.")
            cursor.execute(self.SQL_UPDATE, (
                vo.nombre,
                vo.apellidos,
                vo.contrasena,
                vo.fecha_nacimiento,
                vo.telefono,
                vo.peso_corporal,
                vo.email
            ))
            self.logger.info(f"Usuario {vo.email} actualizado correctamente.")
            return True
        except Exception as e:
            self.logger.error(f"Error al actualizar usuario {vo.email}: {e}")
            return False
        finally:
            cursor.close()