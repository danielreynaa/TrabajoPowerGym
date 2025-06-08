
from src.Modelo.DAO.EntrenamientoDAO import EntrenamientoDAO
from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO
from src.Modelo.DAO.UserDao import UserDao 
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo
from src.Logs.Logger import CustomLogger
from datetime import datetime
from typing import List

class EntrenamientoBO:
    def __init__(self):
        self.entrenamiento_dao = EntrenamientoDAO()
        self.registro_levantamiento_dao = RegistroLevantamientoDAO()
        self.user_dao = UserDao() 
        self.logger = CustomLogger()
        self.logger.info("EntrenamientoBO inicializado.")

    def registrar_entrenamiento_completo(self, email_atleta, ejercicios_data):
        self.logger.info(f"BO: Iniciando registro de entrenamiento para atleta: {email_atleta}.")
        try:
            # --- MODIFICACIÓN CLAVE: Llamar a user_dao.obtener_id_por_email directamente ---
            id_atleta = self.user_dao.obtener_id_por_email(email_atleta) # Simplificado
            if id_atleta is None:
                self.logger.warning(f"BO: No se pudo obtener ID de atleta para {email_atleta}. Abortando registro.")
                return False, "No se encontró el atleta en la base de datos.", [] 
            # --- FIN MODIFICACIÓN ---

            # 2. Crear Entrenamiento principal
            fecha_entreno = datetime.now().strftime("%Y-%m-%d")
            entrenamiento_vo = EntrenamientoVo(id_atleta=id_atleta, fecha_entrenamiento=fecha_entreno, notas=None)
            id_entrenamiento = self.entrenamiento_dao.crear_entrenamiento(entrenamiento_vo)

            if id_entrenamiento is None:
                self.logger.error("BO: Fallo al crear el entrenamiento principal. Abortando registros de levantamientos.")
                return False, "Fallo al crear el entrenamiento principal.", [] 

            # 3. Registrar levantamientos y verificar récords
            nuevos_maximos = []
            for tipo_levantamiento, data in ejercicios_data.items():
                peso = data.get("peso")
                repeticiones = data.get("repeticiones")
                series = data.get("series")
                rpe = data.get("rpe")

                if not peso: 
                    continue

                try:
                    peso_float = float(peso)
                except ValueError:
                    self.logger.warning(f"BO: Peso '{peso}' para {tipo_levantamiento} no es un número válido. Se omitirá este levantamiento.")
                    continue

                maximo_actual = self.registro_levantamiento_dao.obtener_maximo_peso(id_atleta, tipo_levantamiento)
                if peso_float > maximo_actual:
                    nuevos_maximos.append(f"{tipo_levantamiento}: {peso_float} kg")
                    self.logger.info(f"BO: ¡Nuevo récord personal para {tipo_levantamiento}: {peso_float} kg!")

                registro_vo = RegistroLevantamientoVo(
                    id_entrenamiento=id_entrenamiento,
                    tipo_levantamiento=tipo_levantamiento,
                    peso_kg=peso_float,
                    repeticiones=repeticiones,
                    series=series,
                    rpe=rpe if rpe >= 1 and rpe <= 10 else None,
                    id_usuario=id_atleta 
                )
                self.registro_levantamiento_dao.crear_registro(registro_vo)
            
            self.logger.info(f"BO: Entrenamiento completo para atleta {email_atleta} registrado correctamente.")
            return True, "Entrenamiento registrado correctamente.", nuevos_maximos

        except Exception as e:
            self.logger.error(f"BO: Error general al registrar entrenamiento para {email_atleta}: {e}")
            return False, f"Fallo en la lógica de negocio al registrar el entrenamiento: {e}", []
        
    def listar_entrenamientos_asignados(self, id_entrenador: int, id_atleta: int):
        # Si en el futuro filtras por entrenador, aquí lo harás;
        # por ahora devolvemos todos los del atleta.
        return self.listar_entrenamientos_por_atleta(id_atleta)
    
    def listar_entrenamientos_por_atleta(self, id_atleta: int):
        return self.entrenamiento_dao.listar_por_atleta(id_atleta)
    
    def listar_entrenamientos_asignados(self,
                                       id_entrenador: int,
                                       id_atleta:    int
                                      ) -> List[EntrenamientoVo]:
        return self.entrenamiento_dao.listar_por_entrenador_y_atleta(id_entrenador, id_atleta)