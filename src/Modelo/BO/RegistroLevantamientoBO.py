from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo

class RegistroLevantamientoBO:
    def __init__(self):
        self.dao = RegistroLevantamientoDAO()

    def crear_registro(self, registro_vo: RegistroLevantamientoVo) -> bool:
        # Validaciones de negocio (p. ej. peso positivo)
        if registro_vo.peso_kg is None or registro_vo.peso_kg <= 0:
            raise ValueError("El peso debe ser un número positivo.")
        # Delegar al DAO
        return self.dao.crear_registro(registro_vo)

    def listar_historial(self, id_atleta: int) -> list[RegistroLevantamientoVo]:
        # Simple delegación al DAO
        return [
            RegistroLevantamientoVo(
                id_registro=None,
                id_entrenamiento=row[6],  # si tu VO cambió, ajusta posiciones
                id_usuario=id_atleta,
                tipo_levantamiento=row[1],
                peso_kg=row[2],
                repeticiones=row[3],
                series=row[4],
                rpe=row[5]
            )
            for row in self.dao.obtener_historial_levantamientos(id_atleta)
        ]

    def obtener_maximo(self, id_atleta: int, tipo: str) -> float:
        return self.dao.obtener_maximo_peso(id_atleta, tipo)

    def obtener_progreso(self, id_atleta: int, tipo: str) -> tuple[list, list]:
        # Retorna dos listas: fechas y pesos
        datos = self.dao.obtener_registros_para_progreso(id_atleta, tipo)
        fechas  = [row[0] for row in datos]
        pesos   = [row[1] for row in datos]
        return fechas, pesos
