from src.Modelo.BO.EntrenamientoBO import EntrenamientoBO

class ControladorEntrenamiento:
    def __init__(self):
        self.bo = EntrenamientoBO()


    def listar_entrenamientos_asignados(self, id_entrenador: int, id_atleta: int):
        return self.bo.listar_entrenamientos_asignados(id_entrenador, id_atleta)