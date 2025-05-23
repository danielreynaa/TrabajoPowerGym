from src.Modelo.DAO.UserDao import UserDao
from src.Modelo.Conexion import Conexion
from src.Modelo.VO.SuperVo import SuperVo

class BussinessOBject():
SQL_SELECT = "SELECT DNI"


    def consultaLogin(self, loginVo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_CONSULTA)
        result = cursor.fetchall()
        return result 



    def select(self) -> list[SuperVo]:
        cursor = self.get_Cursor()
        usuarios = []


    def pruebaconsulta(self):
        
        userdao = UserDao()
        clientes = userdao.select()


    def comprobarLogin(self, loginVo):
        logindao = UserDao()
        return logindao.consultaLogin(loginVo)















        