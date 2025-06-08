from src.Conexion.Conexion import Conexion
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo
from src.Logs.Logger import CustomLogger

class RegistroLevantamientoDAO:
    def __init__(self):
        self.conexion_db = Conexion()
        self.conn = self.conexion_db.conexion
        self.cursor = self.conn.cursor()
        self.logger = CustomLogger()
        self.logger.info("RegistroLevantamientoDAO inicializado.")

    def crear_registro(self, registro_vo: RegistroLevantamientoVo):
        self.logger.debug(f"DAO: Creando registro de levantamiento para entrenamiento ID {registro_vo.id_entrenamiento}, tipo {registro_vo.tipo_levantamiento}.")
        try:
            self.cursor.execute(
                """INSERT INTO RegistrosLevantamientos (id_entrenamiento, tipo_levantamiento, peso_kg, repeticiones, series, rpe)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (registro_vo.id_entrenamiento, registro_vo.tipo_levantamiento, registro_vo.peso_kg, 
                 registro_vo.repeticiones, registro_vo.series, registro_vo.rpe)
            )
            self.logger.debug(f"DAO: Registro de levantamiento {registro_vo.tipo_levantamiento} insertado correctamente.")
            return True
        except Exception as e:
            self.logger.error(f"DAO: Error al crear registro de levantamiento {registro_vo.tipo_levantamiento} para entrenamiento {registro_vo.id_entrenamiento}: {e}")
            raise # Propagar la excepción

    def obtener_maximo_peso(self, id_atleta, tipo_levantamiento):
        self.logger.debug(f"DAO: Obteniendo máximo peso para atleta {id_atleta}, tipo {tipo_levantamiento}.")
        try:
            self.cursor.execute("""
                SELECT MAX(r.peso_kg)
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
            """, (id_atleta, tipo_levantamiento))
            resultado = self.cursor.fetchone()
            max_peso = resultado[0] if resultado and resultado[0] is not None else 0
            self.logger.debug(f"DAO: Máximo peso para {tipo_levantamiento} de atleta {id_atleta} es {max_peso} kg.")
            return max_peso
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener máximo peso para atleta {id_atleta}, tipo {tipo_levantamiento}: {e}")
            raise # Propagar la excepción
            
    def obtener_registros_para_progreso(self, id_atleta, tipo_levantamiento):
        self.logger.debug(f"DAO: Obteniendo registros para gráfica de progreso para atleta {id_atleta}, tipo {tipo_levantamiento} (máximo por fecha).")
        try:
            self.cursor.execute("""
                SELECT e.fecha_entrenamiento, MAX(r.peso_kg) AS max_peso_dia
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ? AND r.tipo_levantamiento = ?
                GROUP BY e.fecha_entrenamiento 
                ORDER BY e.fecha_entrenamiento ASC
            """, (id_atleta, tipo_levantamiento))
            datos = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(datos)} registros de progreso (máximo por fecha) obtenidos para gráfica de {tipo_levantamiento}.")
            return datos
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener registros para gráfica de progreso para atleta {id_atleta}, tipo {tipo_levantamiento}: {e}")
            raise # Propagar la excepción

    def obtener_historial_levantamientos(self, id_atleta):
        self.logger.debug(f"DAO: Obteniendo historial completo de levantamientos para atleta {id_atleta}.")
        try:
            self.cursor.execute("""
                SELECT e.fecha_entrenamiento, r.tipo_levantamiento, r.peso_kg, r.repeticiones, r.series, r.rpe, e.id_entrenamiento
                FROM Entrenamientos e
                JOIN RegistrosLevantamientos r ON e.id_entrenamiento = r.id_entrenamiento
                WHERE e.id_atleta = ?
                ORDER BY e.fecha_entrenamiento DESC, e.id_entrenamiento DESC
            """, (id_atleta,))
            registros = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(registros)} registros de historial obtenidos para atleta {id_atleta}.")
            return registros
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener historial completo de levantamientos para atleta {id_atleta}: {e}")
            raise # Propagar la excepción