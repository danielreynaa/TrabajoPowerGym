class RegistroLevantamientoVo:
    def __init__(self,
                 id_registro: int = None,
                 id_entrenamiento: int = None,
                 id_usuario: int = None,              # ← nuevo
                 tipo_levantamiento: str = None,
                 peso_kg: float = None,
                 repeticiones: int = None,
                 series: int = None,
                 rpe: float = None):
        self.id_registro        = id_registro
        self.id_entrenamiento   = id_entrenamiento
        self.id_usuario         = id_usuario
        self.tipo_levantamiento = tipo_levantamiento
        self.peso_kg            = peso_kg
        self.repeticiones       = repeticiones
        self.series             = series
        self.rpe                = rpe

    def __str__(self):
        return (f"[Registro {self.id_registro}] Usuario {self.id_usuario} · "
                f"Entreno {self.id_entrenamiento} · {self.tipo_levantamiento}: "
                f"{self.peso_kg}kg x{self.series}x{self.repeticiones} (RPE {self.rpe})")
