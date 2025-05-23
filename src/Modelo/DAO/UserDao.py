from src.Modelo.Conexion import Conexion
from src.Modelo.VO.SuperVo import SuperVo
from typing import List


class UserDao(Conexion):
    SQL_SELECT = "SELECT  DNI, NombreCompleto, Telefono, FechaNacimiento"
    super().__init__()


    def select(self) -> List[SuperVo]:
        cursor = self.getCursor()
        clientes = []

        try:
            cursor.execute(SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                DNI, NombreCompleto, Telefono, FechaNacimiento = row 
                cliente =SuperVo(DNI, NombreCompleto, Telefono, FechaNacimiento)
                clientes.append(cliente)

        except Exception as e: 
            print("e")

        return clientes