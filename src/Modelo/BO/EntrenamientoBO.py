from src.Modelo.DAO.EntrenamientoDAO import EntrenamientoDAO
from src.Modelo.DAO.RegistroLevantamientoDAO import RegistroLevantamientoDAO
from src.Modelo.DAO.UserDao import UserDao
from src.Modelo.VO.EntrenamientoVo import EntrenamientoVo
from src.Modelo.VO.MovimientoVo import MovimientoVo
from src.Modelo.VO.RegistroLevantamientoVo import RegistroLevantamientoVo
from src.Logs.Logger import CustomLogger
from datetime import datetime
from typing import List, Tuple

class EntrenamientoBO:
    def __init__(self):
        self.entrenamiento_dao = EntrenamientoDAO()
        self.registro_dao      = RegistroLevantamientoDAO()
        self.user_dao          = UserDao()
        self.logger            = CustomLogger(log_file="app_powergym.log", log_level="DEBUG")
        self.logger.info("EntrenamientoBO inicializado.")

    def crear_entrenamiento(
        self,
        id_atleta: int,
        id_entrenador: int,
        fecha_entrenamiento: str,
        notas: str = None
    ) -> int:
        vo = EntrenamientoVo(
            id_entrenamiento=None,
            id_atleta=id_atleta,
            id_entrenador=id_entrenador,
            fecha_entrenamiento=fecha_entrenamiento,
            notas=notas
        )
        return self.entrenamiento_dao.crear_entrenamiento(vo)

    def registrar_entrenamiento_completo(
        self,
        email_atleta: str,
        id_entrenador: int,
        ejercicios_data: dict
    ) -> Tuple[bool, str, List[str]]:
        self.logger.info(f"BO: registro completo para {email_atleta}")
        try:
            # 1) obtengo ID atleta
            id_atleta = self.user_dao.obtener_id_por_email(email_atleta)
            if id_atleta is None:
                return False, "Atleta no encontrado.", []

            # 2) creo sesión
            fecha = datetime.now().strftime("%Y-%m-%d")
            vo_ent = EntrenamientoVo(None, id_atleta, id_entrenador, fecha, None)
            id_sesion = self.entrenamiento_dao.crear_entrenamiento(vo_ent)
            if id_sesion is None:
                return False, "Error al crear sesión.", []

            # 3) registro levantamientos
            nuevos_max = []
            for tipo, data in ejercicios_data.items():
                try:
                    peso = float(data.get("peso", 0))
                except:
                    continue
                reps   = data.get("repeticiones", 0)
                series = data.get("series", 0)
                rpe    = data.get("rpe", None)

                max_ant = self.registro_dao.obtener_maximo_peso(id_atleta, tipo)
                if peso > max_ant:
                    nuevos_max.append(f"{tipo}: {peso} kg")

                vo_reg = RegistroLevantamientoVo(
                    id_registro=None,
                    id_entrenamiento=id_sesion,
                    tipo_levantamiento=tipo,
                    peso_kg=peso,
                    repeticiones=reps,
                    series=series,
                    rpe=(rpe if isinstance(rpe, (int, float)) and 1 <= rpe <= 10 else None)
                )
                self.registro_dao.crear_registro(vo_reg)

            return True, "Entrenamiento registrado.", nuevos_max

        except Exception as e:
            self.logger.error(f"BO: excepción → {e}")
            return False, f"Error al registrar: {e}", []

    def listar_entrenamientos_por_atleta(self, id_atleta: int) -> List[EntrenamientoVo]:
        return self.entrenamiento_dao.listar_por_atleta(id_atleta)

    def listar_entrenamientos_asignados(self, id_entrenador: int, id_atleta: int) -> List[EntrenamientoVo]:
        return self.entrenamiento_dao.listar_por_entrenador_y_atleta(id_entrenador, id_atleta)

    def listar_movimientos_por_sesion(self, id_entrenamiento: int) -> List[MovimientoVo]:
        return self.entrenamiento_dao.listar_movimientos_por_sesion(id_entrenamiento)
