
class RegistroLevantamientoVo:
    def __init__(self, id_registro=None, id_entrenamiento=None, tipo_levantamiento=None, 
                 peso_kg=None, repeticiones=None, series=None, rpe=None):
        self.id_registro = id_registro
        self.id_entrenamiento = id_entrenamiento
        self.tipo_levantamiento = tipo_levantamiento
        self.peso_kg = peso_kg
        self.repeticiones = repeticiones
        self.series = series
        self.rpe = rpe

    def to_dict(self):
        return {
            "id_registro": self.id_registro,
            "id_entrenamiento": self.id_entrenamiento,
            "tipo_levantamiento": self.tipo_levantamiento,
            "peso_kg": self.peso_kg,
            "repeticiones": self.repeticiones,
            "series": self.series,
            "rpe": self.rpe
        }