
from src.Modelo.DAO.UserDao import UserDao # Para obtener el ID del usuario
from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO # Para obtener los datos de levantamientos
from src.Logs.Logger import CustomLogger

class ProgresoBO:
    def __init__(self):
        self.user_dao = UserDao()
        self.registro_levantamiento_dao = RegistroLevantamientoDAO()
        self.logger = CustomLogger()
        self.logger.info("ProgresoBO inicializado.")

    def obtener_datos_para_grafica(self, email_atleta, tipo_levantamiento):
        self.logger.info(f"BO: Obteniendo datos para gráfica de {tipo_levantamiento} para atleta: {email_atleta}.")
        try:
            # 1. Obtener id_atleta
            usuario_data = self.user_dao.obtener_usuario_por_email(email_atleta)
            if usuario_data and 'id_usuario' in usuario_data:
                id_atleta = usuario_data['id_usuario']
            else:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. No se puede generar la gráfica.")
                return None, "No se encontró el atleta en la base de datos."

            # 2. Obtener registros de levantamientos
            datos_brutos = self.registro_levantamiento_dao.obtener_registros_para_progreso(id_atleta, tipo_levantamiento)

            # Formatear datos para la gráfica (fechas y pesos)
            fechas = [str(x[0]) for x in datos_brutos] # Convertir fecha a string
            pesos = [float(x[1]) for x in datos_brutos] # Convertir peso a float

            self.logger.info(f"BO: Datos de gráfica para {tipo_levantamiento} obtenidos: {len(fechas)} puntos.")
            return fechas, pesos
        except Exception as e:
            self.logger.error(f"BO: Error al obtener datos para gráfica de progreso de {tipo_levantamiento} para {email_atleta}: {e}")
            return None, f"Fallo al cargar datos para la gráfica: {e}"