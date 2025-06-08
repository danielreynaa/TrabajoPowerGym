from src.Modelo.BO.EntrenamientoBO import EntrenamientoBO
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from typing import List


class ControladorEntrenamiento:
    def __init__(self):
        self.bo = EntrenamientoBO()


    def listar_entrenamientos_asignados(self, id_entrenador: int,id_atleta:int) -> List[EntrenamientoVo]:
        return self.bo.listar_entrenamientos_asignados(id_entrenador, id_atleta)