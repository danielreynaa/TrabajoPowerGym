from src.Conexion.Conexion import Conexion
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Logs.Logger import CustomLogger
from typing import List

class EntrenamientoDAO(Conexion):
    SQL_LISTAR_POR_ATLETA = """
        SELECT id_entrenamiento,
               id_atleta,
               fecha_entrenamiento,
               notas
          FROM Entrenamientos
         WHERE id_atleta = ?
      ORDER BY fecha_entrenamiento DESC
    """

    def __init__(self):
        super().__init__()  # Inicializa self.conexion
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info("EntrenamientoDAO: inicializado.")

    def crear_entrenamiento(self, vo: EntrenamientoVo) -> int:
        cursor = self.getCursor()
        try:
            self.logger.debug(
                f"DAO: Insertando Entrenamiento para atleta {vo.id_atleta} en {vo.fecha_entrenamiento}"
            )
            cursor.execute(
                "INSERT INTO Entrenamientos (id_atleta, fecha_entrenamiento, notas) VALUES (?, ?, ?)",
                (vo.id_atleta, vo.fecha_entrenamiento, vo.notas)
            )
            # Obtener ID generado
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()

    def listar_por_atleta(self, id_atleta: int) -> List[EntrenamientoVo]:
        cursor = self.getCursor()
        sesiones: List[EntrenamientoVo] = []
        try:
            cursor.execute(self.SQL_LISTAR_POR_ATLETA, (id_atleta,))
            rows = cursor.fetchall()
            self.logger.debug(f"DAO: {len(rows)} sesiones obtenidas para atleta {id_atleta}.")
            for row in rows:
                sesiones.append(EntrenamientoVo(*row))
        finally:
            cursor.close()
        return sesiones
