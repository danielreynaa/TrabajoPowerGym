# src/Modelo/DAO/UserDao.py
from src.Modelo.Conexion.Conexion import Conexion
from src.Modelo.VO.SuperVo import SuperVo
from typing import List

class UserDao(Conexion):
    SQL_SELECT = """
        SELECT id_usuario,
               nombre, apellidos, email, contrasena, rol,
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

    def __init__(self):
        super().__init__()

    def select(self) -> List[SuperVo]:
        cursor = self.getCursor()
        usuarios: List[SuperVo] = []
        try:
            cursor.execute(self.SQL_SELECT)
            for row in cursor.fetchall():
                # row = (id_usuario, nombre, apellidos, email, contrasena, rol,
                #        fecha_registro, fecha_nacimiento, telefono, peso_corporal)
                usuarios.append(SuperVo(*row))
        except Exception as e:
            print("❌ Error en SELECT:", e)
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
            self.conexion.commit()
            print("✅ Usuario insertado correctamente.")
        except Exception as e:
            print("❌ Error al INSERT:", e)
        finally:
            cursor.close()

    def consulta_login(self, email: str, contrasena: str) -> bool:
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CONSULTA_LOGIN, (email, contrasena))
            count = cursor.fetchone()[0]
            return count == 1
        except Exception as e:
            print("❌ Error en login:", e)
            return False
        finally:
            cursor.close()
