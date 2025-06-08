from src.Conexion.Conexion import Conexion
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Logs.Logger import CustomLogger
from typing import List

class EntrenamientoDAO(Conexion):
    SQL_INSERT = """
        INSERT INTO Entrenamientos 
           (id_atleta, id_entrenador, fecha_entrenamiento, notas)
        VALUES (?, ?, ?, ?)
    """
    SQL_LAST_ID = "SELECT LAST_INSERT_ID()"
    SQL_LISTAR_POR_ATLETA = """
        SELECT id_entrenamiento,
               id_atleta,
               id_entrenador,
               fecha_entrenamiento,
               notas
          FROM Entrenamientos
         WHERE id_atleta = ?
      ORDER BY fecha_entrenamiento DESC
    """
    SQL_LISTAR_POR_ENTRENADOR_Y_ATLETA = """
        SELECT id_entrenamiento,
               id_atleta,
               id_entrenador,
               fecha_entrenamiento,
               notas
          FROM Entrenamientos
         WHERE id_atleta     = ?
           AND id_entrenador = ?
      ORDER BY fecha_entrenamiento DESC
    """

    def __init__(self):
        super().__init__()  
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info("EntrenamientoDAO inicializado.")

    def crear_entrenamiento(self, vo: EntrenamientoVo) -> int:
        cursor = self.getCursor()
        try:
            self.logger.debug(
                f"DAO: insertando sesión atleta={vo.id_atleta}, "
                f"entrenador={vo.id_entrenador}, fecha={vo.fecha_entrenamiento}"
            )
            cursor.execute(self.SQL_INSERT, (
                vo.id_atleta,
                vo.id_entrenador,
                vo.fecha_entrenamiento,
                vo.notas
            ))
            cursor.execute(self.SQL_LAST_ID)
            row = cursor.fetchone()
            id_ent = row[0] if row else None
            self.logger.debug(f"DAO: sesión insertada con ID={id_ent}")
            return id_ent
        except Exception as e:
            self.logger.error(f"DAO: error al crear entrenamiento: {e}")
            raise
        finally:
            cursor.close()

    def listar_por_atleta(self, id_atleta: int) -> List[EntrenamientoVo]:
        cursor = self.getCursor()
        sesiones: List[EntrenamientoVo] = []
        try:
            cursor.execute(self.SQL_LISTAR_POR_ATLETA, (id_atleta,))
            rows = cursor.fetchall()
            self.logger.debug(f"DAO: {len(rows)} sesiones para atleta {id_atleta}")
            for row in rows:
                sesiones.append(EntrenamientoVo(*row))
            return sesiones
        finally:
            cursor.close()

    def listar_por_entrenador_y_atleta(self, id_entrenador: int, id_atleta: int) -> List[EntrenamientoVo]:
        cursor = self.getCursor()
        sesiones: List[EntrenamientoVo] = []
        try:
            cursor.execute(self.SQL_LISTAR_POR_ENTRENADOR_Y_ATLETA, (id_atleta, id_entrenador))
            rows = cursor.fetchall()
            self.logger.debug(
                f"DAO: {len(rows)} sesiones para entrenador={id_entrenador}, atleta={id_atleta}"
            )
            for row in rows:
                sesiones.append(EntrenamientoVo(*row))
            return sesiones
        finally:
            cursor.close()
