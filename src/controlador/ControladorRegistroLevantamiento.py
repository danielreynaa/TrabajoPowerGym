from src.Modelo.BO.RegistroLevantamientoBO import RegistroLevantamientoBO
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo

class ControladorRegistroLevantamiento:
    def __init__(self):
        self.bo = RegistroLevantamientoBO()

    def registrar_levantamiento(
        self,
        id_entrenamiento: int,
        id_usuario:       int,
        tipo:             str,
        peso_kg:          float,
        repeticiones:     int,
        series:           int,
        rpe:              float = None
    ) -> bool:
        vo = RegistroLevantamientoVo(
            id_entrenamiento=id_entrenamiento,
            id_usuario=id_usuario,
            tipo_levantamiento=tipo,
            peso_kg=peso_kg,
            repeticiones=repeticiones,
            series=series,
            rpe=rpe
        )
        return self.bo.crear_registro(vo)

    def listar_historial(self, id_atleta: int) -> list[RegistroLevantamientoVo]:
        return self.bo.listar_historial(id_atleta)

    def obtener_maximo(self, id_atleta: int, tipo: str) -> float:
        return self.bo.obtener_maximo(id_atleta, tipo)

    def obtener_progreso(self, id_atleta: int, tipo: str) -> tuple[list, list]:
        return self.bo.obtener_progreso(id_atleta, tipo)

    def listar_movimientos_por_sesion(self, id_sesion: int):
        return self.bo.listar_movimientos_por_sesion(id_sesion)

