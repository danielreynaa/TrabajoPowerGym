class EntrenamientoVo:
    def __init__(self,
                 id_entrenamiento:    int,
                 id_atleta:           int,
                 fecha_entrenamiento: str,   # o datetime.date si prefieres
                 notas:               str = None):
        self.id_entrenamiento    = id_entrenamiento
        self.id_atleta           = id_atleta
        self.fecha_entrenamiento = fecha_entrenamiento
        self.notas               = notas

    def __str__(self):
        return f"[{self.fecha_entrenamiento}] {self.notas or ''}"
