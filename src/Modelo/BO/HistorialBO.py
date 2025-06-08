# C:\Users\elded\OneDrive\Escritorio\INGENIERÍA DE SOFTWARE\POWER GYM\TrabajoPowerGym\src\Modelo\BO\HistorialBO.py

from src.Modelo.DAO.UserDao import UserDao 
from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO 
from src.Logs.Logger import CustomLogger

class HistorialBO:
    def __init__(self):
        self.user_dao = UserDao()
        self.registro_levantamiento_dao = RegistroLevantamientoDAO()
        self.logger = CustomLogger()
        self.logger.info("HistorialBO inicializado.")

    # --- MÉTODO OBTENER HISTORIAL COMPLETO ---
    def obtener_historial_completo_atleta(self, email_atleta):
        self.logger.info(f"BO: Obteniendo historial completo para atleta: {email_atleta}.")
        try:
            id_atleta = self.user_dao.obtener_id_por_email(email_atleta) # Llama al método correcto en UserDao
            if id_atleta is None:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. No se puede cargar el historial.")
                return None, "No se encontró el atleta en la base de datos."

            historial_data = self.registro_levantamiento_dao.obtener_historial_levantamientos(id_atleta)

            self.logger.info(f"BO: Historial completo para atleta {email_atleta} obtenido: {len(historial_data)} registros.")
            return historial_data, None 
        except Exception as e:
            self.logger.error(f"BO: Error al obtener historial completo para atleta {email_atleta}: {e}")
            return None, f"Fallo al cargar el historial: {e}"

    # --- MÉTODO OBTENER RÉCORDS ---
    def obtener_records_atleta(self, email_atleta):
        self.logger.info(f"BO: Obteniendo récords para atleta: {email_atleta}.")
        try:
            id_atleta = self.user_dao.obtener_id_por_email(email_atleta) # Llama al método correcto en UserDao
            if id_atleta is None:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. No se pueden cargar los récords.")
                return {}, "No se encontró el atleta en la base de datos."

            ejercicios = ["Sentadilla", "Banca", "Peso Muerto"]
            records = {}
            for ejercicio in ejercicios:
                max_peso = self.registro_levantamiento_dao.obtener_maximo_peso(id_atleta, ejercicio)
                records[ejercicio] = max_peso

            self.logger.info(f"BO: Récords para atleta {email_atleta} obtenidos: {records}.")
            return records, None 
        except Exception as e:
            self.logger.error(f"BO: Error al obtener récords para atleta {email_atleta}: {e}")
            return {}, f"Fallo al cargar los récords: {e}"

    # --- MÉTODO OBTENER CONTEO DE ENTRENAMIENTOS POR EJERCICIO ---
    def obtener_conteo_entrenamientos_por_ejercicio(self, email_atleta):
        self.logger.info(f"BO: Obteniendo conteo de entrenamientos por ejercicio para atleta: {email_atleta}.")
        try:
            id_atleta = self.user_dao.obtener_id_por_email(email_atleta) # Llama al método correcto en UserDao
            if id_atleta is None:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. No se puede contar los entrenamientos.")
                return {}, "No se encontró el atleta en la base de datos."

            ejercicios = ["Sentadilla", "Banca", "Peso Muerto"]
            conteos = {}
            for ejercicio in ejercicios:
                count = self.registro_levantamiento_dao.contar_entrenamientos_por_ejercicio(id_atleta, ejercicio)
                conteos[ejercicio] = count

            self.logger.info(f"BO: Conteo de entrenamientos por ejercicio para atleta {email_atleta} obtenido: {conteos}.")
            return conteos, None
        except Exception as e:
            self.logger.error(f"BO: Error al obtener conteo de entrenamientos por ejercicio para atleta {email_atleta}: {e}")
            return {}, f"Fallo al cargar los conteos: {e}"