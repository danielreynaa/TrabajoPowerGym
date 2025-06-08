from src.Modelo.BO.EntrenamientoBO import EntrenamientoBO
from typing import List
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo

class ControladorEntrenamiento:
    def __init__(self):
        self.entrenamiento_bo = EntrenamientoBO()

    def crear_sesion(self,
                     id_atleta: int,
                     id_entrenador: int,
                     fecha: str,
                     notas: str = None
    ) -> int:
        return self.entrenamiento_bo.crear_entrenamiento(
            id_atleta, id_entrenador, fecha, notas
        )


    def registrar_entrenamiento_completo(self, email_atleta: str, id_entrenador: int, ejercicios_data: dict):
        return self.entrenamiento_bo.registrar_entrenamiento_completo(email_atleta, id_entrenador, ejercicios_data)

    def listar_entrenamientos_por_atleta(self, id_atleta: int) -> List[EntrenamientoVo]:
        return self.entrenamiento_bo.listar_entrenamientos_por_atleta(id_atleta)

    def listar_entrenamientos_asignados(self, id_entrenador: int, id_atleta: int) -> List[EntrenamientoVo]:
        return self.entrenamiento_bo.listar_entrenamientos_asignados(id_entrenador, id_atleta)
