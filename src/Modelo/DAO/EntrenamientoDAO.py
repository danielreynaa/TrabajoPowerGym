
from src.Conexion.Conexion import Conexion
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Logs.Logger import CustomLogger

class EntrenamientoDAO:
    def __init__(self):
        self.conexion_db = Conexion() # Crea una instancia de Conexión
        self.conn = self.conexion_db.conexion
        self.cursor = self.conn.cursor()
        self.logger = CustomLogger()
        self.logger.info("EntrenamientoDAO inicializado.")

    def crear_entrenamiento(self, entrenamiento_vo: EntrenamientoVo):
        self.logger.debug(f"DAO: Creando nuevo entrenamiento para id_atleta {entrenamiento_vo.id_atleta} en fecha {entrenamiento_vo.fecha_entrenamiento}.")
        try:
            self.cursor.execute(
                "INSERT INTO Entrenamientos (id_atleta, fecha_entrenamiento, notas) VALUES (?, ?, ?)",
                (entrenamiento_vo.id_atleta, entrenamiento_vo.fecha_entrenamiento, entrenamiento_vo.notas)
            )
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            result = self.cursor.fetchone()
            id_entrenamiento = result[0] if result else None

            if id_entrenamiento:
                self.logger.debug(f"DAO: Entrenamiento {id_entrenamiento} insertado correctamente.")
                return id_entrenamiento
            else:
                self.logger.error("DAO: No se pudo obtener el ID del entrenamiento recién insertado.")
                return None
        except Exception as e:
            self.logger.error(f"DAO: Error al crear entrenamiento para atleta {entrenamiento_vo.id_atleta}: {e}")
            raise 