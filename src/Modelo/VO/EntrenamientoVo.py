class EntrenamientoVo:
    def __init__(self, id_entrenamiento=None, id_atleta=None, fecha_entrenamiento=None, notas=None):
        self.id_entrenamiento = id_entrenamiento
        self.id_atleta = id_atleta
        self.fecha_entrenamiento = fecha_entrenamiento
        self.notas = notas

    def to_dict(self):
        return {
            "id_entrenamiento": self.id_entrenamiento,
            "id_atleta": self.id_atleta,
            "fecha_entrenamiento": self.fecha_entrenamiento,
            "notas": self.notas
        }