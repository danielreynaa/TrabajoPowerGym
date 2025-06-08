from src.Conexion.Conexion import Conexion
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo
from src.Logs.Logger import CustomLogger

class RegistroLevantamientoDAO:
    def __init__(self):
        # Conexión a BD
        self.conexion_db = Conexion()
        self.conn       = self.conexion_db.conexion
        self.cursor     = self.conn.cursor()
        # Logger consistente
        self.logger = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info("RegistroLevantamientoDAO: inicializado.")

    def crear_registro(self, registro_vo: RegistroLevantamientoVo) -> bool:
        """
        Inserta un nuevo registro de levantamiento, incluyendo id_usuario.
        Si no tienes sesión de entrenamiento, pasa id_entrenamiento=None y
        asegúrate de que la columna id_entrenamiento acepte NULL.
        """
        self.logger.debug(
            f"DAO: creando levantamiento → "
            f"entrenamiento={registro_vo.id_entrenamiento}, "
            f"usuario={registro_vo.id_usuario}, "
            f"tipo={registro_vo.tipo_levantamiento}, "
            f"peso={registro_vo.peso_kg}kg"
        )
        try:
            self.cursor.execute(
                """
                INSERT INTO RegistrosLevantamientos (
                    id_entrenamiento,
                    id_usuario,
                    tipo_levantamiento,
                    peso_kg,
                    repeticiones,
                    series,
                    rpe
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    registro_vo.id_entrenamiento,
                    registro_vo.id_usuario,
                    registro_vo.tipo_levantamiento,
                    registro_vo.peso_kg,
                    registro_vo.repeticiones,
                    registro_vo.series,
                    registro_vo.rpe
                )
            )
            self.logger.info(
                f"DAO: levantamiento '{registro_vo.tipo_levantamiento}' "
                f"guardado para usuario {registro_vo.id_usuario}."
            )
            return True
        except Exception as e:
            self.logger.error(
                f"DAO: error al crear levantamiento para usuario "
                f"{registro_vo.id_usuario}, entrenamiento "
                f"{registro_vo.id_entrenamiento}: {e}"
            )
            raise

    def obtener_maximo_peso(self, id_atleta: int, tipo_levantamiento: str) -> float:
        self.logger.debug(f"DAO: Obteniendo máximo peso para atleta={id_atleta}, tipo={tipo_levantamiento}.")
        try:
            self.cursor.execute(
                """
                SELECT MAX(r.peso_kg)
                  FROM Entrenamientos e
                  JOIN RegistrosLevantamientos r
                    ON e.id_entrenamiento = r.id_entrenamiento
                 WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
                """,
                (id_atleta, tipo_levantamiento)
            )
            resultado = self.cursor.fetchone()
            max_peso = resultado[0] or 0.0
            self.logger.debug(f"DAO: Máximo peso para {tipo_levantamiento} de atleta {id_atleta} = {max_peso} kg.")
            return max_peso
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener máximo peso: {e}")
            raise

    def obtener_registros_para_progreso(self, id_atleta: int, tipo_levantamiento: str):
        self.logger.debug(f"DAO: Obteniendo datos de progreso para atleta={id_atleta}, tipo={tipo_levantamiento}.")
        try:
            self.cursor.execute(
                """
                SELECT e.fecha_entrenamiento, MAX(r.peso_kg) AS max_peso_dia
                  FROM Entrenamientos e
                  JOIN RegistrosLevantamientos r
                    ON e.id_entrenamiento = r.id_entrenamiento
                 WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
                 GROUP BY e.fecha_entrenamiento
                 ORDER BY e.fecha_entrenamiento ASC
                """,
                (id_atleta, tipo_levantamiento)
            )
            datos = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(datos)} puntos de progreso obtenidos.")
            return datos
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener registros de progreso: {e}")
            raise

    def obtener_historial_levantamientos(self, id_atleta: int):
        self.logger.debug(f"DAO: Obteniendo historial completo de levantamientos para atleta={id_atleta}.")
        try:
            self.cursor.execute(
                """
                SELECT 
                  e.fecha_entrenamiento,
                  r.tipo_levantamiento,
                  r.peso_kg,
                  r.repeticiones,
                  r.series,
                  r.rpe,
                  e.id_entrenamiento
                  -- r.id_usuario ya no hace falta aquí
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r
                  ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ?
                ORDER BY e.fecha_entrenamiento DESC, e.id_entrenamiento DESC
                """,
                (id_atleta,)
            )
            registros = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(registros)} registros de historial obtenidos.")
            return registros
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener historial de levantamientos: {e}")
            raise
