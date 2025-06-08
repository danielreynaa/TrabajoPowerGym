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
        self.logger.debug(f"DAO: Creando registro de levantamiento para entrenamiento ID {registro_vo.id_entrenamiento}, tipo {registro_vo.tipo_levantamiento}, usuario ID {registro_vo.id_usuario}.")
        try:
            self.cursor.execute(
                """INSERT INTO RegistrosLevantamientos (id_entrenamiento, tipo_levantamiento, peso_kg, repeticiones, series, rpe, id_usuario)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (registro_vo.id_entrenamiento, registro_vo.tipo_levantamiento, registro_vo.peso_kg, 
                 registro_vo.repeticiones, registro_vo.series, registro_vo.rpe, registro_vo.id_usuario)
            )
            self.logger.debug(f"DAO: Registro de levantamiento {registro_vo.tipo_levantamiento} insertado correctamente.")
            return True
        except Exception as e:
            self.logger.error(f"DAO: Error al crear registro de levantamiento {registro_vo.tipo_levantamiento} para entrenamiento {registro_vo.id_entrenamiento}, usuario {registro_vo.id_usuario}: {e}")
            raise 

    def obtener_maximo_peso(self, id_atleta, tipo_levantamiento):
        self.logger.debug(f"DAO: Obteniendo máximo peso para atleta {id_atleta}, tipo {tipo_levantamiento}.")
        try:
            self.cursor.execute("""
                SELECT MAX(peso_kg)
                FROM RegistrosLevantamientos
                WHERE id_usuario = ? AND tipo_levantamiento = ?
            """, (id_atleta, tipo_levantamiento))
            resultado = self.cursor.fetchone()
            max_peso = resultado[0] if resultado and resultado[0] is not None else 0
            self.logger.debug(f"DAO: Máximo peso para {tipo_levantamiento} de atleta {id_atleta} es {max_peso} kg.")
            return max_peso
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener máximo peso para atleta {id_atleta}, tipo {tipo_levantamiento}: {e}")
            raise 

    def obtener_registros_para_progreso(self, id_atleta, tipo_levantamiento):
        self.logger.debug(f"DAO: Obteniendo registros para gráfica de progreso para atleta {id_atleta}, tipo {tipo_levantamiento} (máximo por fecha).")
        try:
            self.cursor.execute("""
                SELECT E.fecha_entrenamiento, MAX(RL.peso_kg) AS max_peso_dia
                FROM RegistrosLevantamientos RL
                JOIN Entrenamientos E ON RL.id_entrenamiento = E.id_entrenamiento
                WHERE RL.id_usuario = ? AND RL.tipo_levantamiento = ? 
                GROUP BY E.fecha_entrenamiento 
                ORDER BY E.fecha_entrenamiento ASC
            """, (id_atleta, tipo_levantamiento))
            datos = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(datos)} registros de progreso (máximo por fecha) obtenidos para gráfica de {tipo_levantamiento}.")
            return datos
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener registros para gráfica de progreso para atleta {id_atleta}, tipo {tipo_levantamiento}: {e}")
            raise 

    def obtener_historial_levantamientos(self, id_atleta):
        self.logger.debug(f"DAO: Obteniendo historial completo de levantamientos para atleta {id_atleta}.")
        try:
            self.cursor.execute("""
                SELECT E.fecha_entrenamiento, RL.tipo_levantamiento, RL.peso_kg, RL.repeticiones, RL.series, RL.rpe, RL.id_entrenamiento
                FROM RegistrosLevantamientos RL 
                JOIN Entrenamientos E ON RL.id_entrenamiento = E.id_entrenamiento 
                WHERE RL.id_usuario = ? 
                ORDER BY E.fecha_entrenamiento DESC, RL.id_entrenamiento DESC
            """, (id_atleta,))
            registros = self.cursor.fetchall()
            self.logger.debug(f"DAO: {len(registros)} registros de historial obtenidos para atleta {id_atleta}.")
            return registros
        except Exception as e:
            self.logger.error(f"DAO: Error al obtener historial completo de levantamientos para atleta {id_atleta}: {e}")
            raise 
    def contar_entrenamientos_por_ejercicio(self, id_atleta, tipo_levantamiento):
        self.logger.debug(f"DAO: Intentando contar entrenamientos para ID_USUARIO: {id_atleta}, TIPO: '{tipo_levantamiento}'.")
        try:
            self.cursor.execute("""
                SELECT COUNT(RL.id_registro)
                FROM RegistrosLevantamientos RL
                WHERE RL.id_usuario = ? AND RL.tipo_levantamiento = ?
            """, (id_atleta, tipo_levantamiento))
            count = self.cursor.fetchone()[0]
            self.logger.debug(f"DAO: COUNT SQL DEVOLVIÓ: {count} para tipo '{tipo_levantamiento}' y usuario ID {id_atleta}.")
            return count
        except Exception as e:
            self.logger.error(f"DAO: Error al contar entrenamientos de {tipo_levantamiento} para atleta {id_atleta}: {e}")
            raise 