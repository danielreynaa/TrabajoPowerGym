from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO
from src.Modelo.DAO.EntrenamientoDAO import EntrenamientoDAO
from src.Modelo.DAO.UserDao import UserDao # AHORA USA EL UserDao EXISTENTE
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo
from src.Logs.Logger import CustomLogger
from datetime import datetime

class EntrenamientoBO:
    def __init__(self):
        self.entrenamiento_dao = EntrenamientoDAO()
        self.registro_levantamiento_dao = RegistroLevantamientoDAO()
        self.user_dao = UserDao() # AHORA USA EL UserDao EXISTENTE
        self.logger = CustomLogger()
        self.logger.info("EntrenamientoBO inicializado.")

    def registrar_entrenamiento_completo(self, email_atleta, ejercicios_data):
        """
        Registra un entrenamiento completo con todos sus levantamientos.
        email_atleta: Email del usuario Atleta.
        ejercicios_data: Diccionario con los datos de cada ejercicio (peso, repeticiones, series, rpe).
                        Ej: {"Sentadilla": {"peso": "100", "repeticiones": 5, "series": 5, "rpe": 8}, ...}
        """
        self.logger.info(f"BO: Iniciando registro de entrenamiento para atleta: {email_atleta}.")
        try:
            # 1. Obtener id_atleta
            usuario_data = self.user_dao.obtener_usuario_por_email(email_atleta)
            if usuario_data and 'id_usuario' in usuario_data:
                id_atleta = usuario_data['id_usuario']
            else:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. Abortando registro.")
                return False, "No se encontró el atleta en la base de datos.", [] # Devuelve lista vacía para nuevos_maximos

            # 2. Crear Entrenamiento principal
            fecha_entreno = datetime.now().strftime("%Y-%m-%d")
            entrenamiento_vo = EntrenamientoVo(id_atleta=id_atleta, fecha_entrenamiento=fecha_entreno, notas=None)
            id_entrenamiento = self.entrenamiento_dao.crear_entrenamiento(entrenamiento_vo)

            if id_entrenamiento is None:
                self.logger.error("BO: Fallo al crear el entrenamiento principal. Abortando registros de levantamientos.")
                return False, "Fallo al crear el entrenamiento principal.", [] # Devuelve lista vacía para nuevos_maximos

            # 3. Registrar levantamientos y verificar récords
            nuevos_maximos = []
            for tipo_levantamiento, data in ejercicios_data.items():
                peso = data.get("peso")
                repeticiones = data.get("repeticiones")
                series = data.get("series")
                rpe = data.get("rpe")

                if not peso: # Si el campo de peso está vacío, no se registra este levantamiento
                    continue

                try:
                    peso_float = float(peso)
                except ValueError:
                    self.logger.warning(f"BO: Peso '{peso}' para {tipo_levantamiento} no es un número válido. Se omitirá este levantamiento.")
                    continue

                # Obtener máximo actual para verificar nuevo récord
                maximo_actual = self.registro_levantamiento_dao.obtener_maximo_peso(id_atleta, tipo_levantamiento)
                if peso_float > maximo_actual:
                    nuevos_maximos.append(f"{tipo_levantamiento}: {peso_float} kg")
                    self.logger.info(f"BO: ¡Nuevo récord personal para {tipo_levantamiento}: {peso_float} kg!")

                # Crear VO para el registro del levantamiento
                registro_vo = RegistroLevantamientoVo(
                    id_entrenamiento=id_entrenamiento,
                    tipo_levantamiento=tipo_levantamiento,
                    peso_kg=peso_float,
                    repeticiones=repeticiones,
                    series=series,
                    rpe=rpe if rpe >= 1 and rpe <= 10 else None # RPE solo si está en el rango
                )
                self.registro_levantamiento_dao.crear_registro(registro_vo)

            self.logger.info(f"BO: Entrenamiento completo para atleta {email_atleta} registrado correctamente.")
            return True, "Entrenamiento registrado correctamente.", nuevos_maximos

        except Exception as e:
            self.logger.error(f"BO: Error general al registrar entrenamiento para {email_atleta}: {e}")
            return False, f"Fallo en la lógica de negocio al registrar el entrenamiento: {e}", [] # Devuelve lista vacía para nuevos_maximos