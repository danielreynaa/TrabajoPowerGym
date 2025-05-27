class SuperVo:
    def __init__(self,
                 id_usuario: int,
                 nombre: str,
                 apellidos: str,
                 email: str,
                 contrasena: str,
                 rol: str,
                 fecha_registro: str,
                 fecha_nacimiento: str = None,
                 telefono: str = None,
                 peso_corporal: float = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.contrasena = contrasena
        self.rol = rol
        self.fecha_registro = fecha_registro
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.peso_corporal = peso_corporal

    def __str__(self):
        return (f"[{self.id_usuario}] {self.nombre} {self.apellidos} | "
                f"{self.email} | Rol: {self.rol} | Registrado: {self.fecha_registro}")
