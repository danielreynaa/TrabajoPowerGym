from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import hashlib
from datetime import date

from src.Vista.VistaLogin import Login
from src.Modelo.BO.UserBO import UserBO
from src.Logs.Logger import CustomLogger

Form_Registro, _ = uic.loadUiType("./src/Vista/Ui/VistaRegistro.ui")

class VistaRegistro(QMainWindow, Form_Registro):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # >>>>>> CAMBIO 1: Logger - Obtener la instancia existente sin reconfigurar <<<<<<
        # CustomLogger es un Singleton. Ya está inicializado en main.py.
        # No le pases argumentos aquí para obtener la misma instancia configurada.
        self.logger = CustomLogger() 
        self.logger.info("VistaRegistro: inicializada.")

        # Conexiones de los botones
        self.btn_registrar.clicked.connect(self.procesar_registro)
        self.btn_volver_login.clicked.connect(self.volver_a_login)

    def procesar_registro(self):
        nombre           = self.txt_nombre.text().strip()
        apellidos        = self.txt_apellidos.text().strip()
        email            = self.txt_email.text().strip()
        contrasena       = self.txt_password.text()
        confirm_contrasena = self.txt_confirm_password.text()
        
        # >>>>>> CAMBIO 2: Normalizar la capitalización del rol <<<<<<
        # Mapeo para asegurar que el rol tenga la capitalización exacta del ENUM de la base de datos
        rol_input = self.combo_rol.currentText().strip() # Leer el texto de la UI
        rol_mapeado = {
            "administrador": "Administrador",
            "entrenador":    "Entrenador",
            "atleta":        "Atleta"
        }.get(rol_input.lower(), "") # Convertir a minúsculas para el mapeo, y si no se encuentra, dejar vacío para el error
        
        rol = rol_mapeado # Usaremos este rol mapeado para la inserción
        self.logger.debug(f"VistaRegistro: Rol de UI '{rol_input}' mapeado a '{rol}' para inserción.")

        fecha_qdate      = self.dateedit_fecha_nacimiento.date()
        fecha_nac        = fecha_qdate.toString("yyyy-MM-dd") if fecha_qdate.isValid() else None
        telefono         = self.txt_telefono.text().strip()
        peso_corp        = self.spinbox_peso_corporal.value() if self.spinbox_peso_corporal.value() > 0 else None

        errores = []
        if not nombre:
            errores.append("El Nombre es obligatorio.")
        if not apellidos:
            errores.append("Los Apellidos son obligatorios.")
        if not email:
            errores.append("El Correo Electrónico es obligatorio.")
        elif "@" not in email or "." not in email:
            errores.append("El formato del Correo Electrónico no es válido.")
        if not contrasena:
            errores.append("La Contraseña es obligatoria.")
        if not confirm_contrasena:
            errores.append("La Confirmación de Contraseña es obligatoria.")
        if contrasena != confirm_contrasena:
            errores.append("Las contraseñas no coinciden.")
        
        # >>>>>> CAMBIO 3: Validar que el rol mapeado no esté vacío <<<<<<
        # Si rol_mapeado es "", significa que el texto de la UI no coincidió con ningún rol conocido
        if not rol: # Ahora validamos 'rol' después del mapeo
            errores.append("Debe seleccionar un tipo de usuario válido.")

        if errores:
            msg = "; ".join(errores)
            self.logger.warning(f"VistaRegistro: validación fallida para '{email}' → {msg}")
            QMessageBox.warning(self, "Error de Registro", "\n".join(errores))
            return

        # Hash de la contraseña
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        user_bo = UserBO()

        try:
            self.logger.debug(f"VistaRegistro: Llamando a user_bo.registrar_usuario con email={email}, rol={rol}, peso_corporal={peso_corp}.") # Log detallado
            user_bo.registrar_usuario(
                nombre=nombre,
                apellidos=apellidos,
                email=email,
                contrasena=contrasena_hash,
                rol=rol, # Usar el rol mapeado aquí
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                peso_corporal=peso_corp
            )
            self.logger.info(f"VistaRegistro: usuario '{email}' registrado exitosamente con rol '{rol}'.")
            QMessageBox.information(
                self, "Registro Exitoso",
                "¡Usuario registrado correctamente! Ahora puede iniciar sesión."
            )
            self.volver_a_login()

        except Exception as e:
            self.logger.error(f"VistaRegistro: error al registrar '{email}' → {e}")
            QMessageBox.critical(
                self, "Error de Registro",
                f"No se pudo registrar el usuario: {e}"
            )
            self.txt_password.clear()
            self.txt_confirm_password.clear()

    def volver_a_login(self):
        self.logger.info("VistaRegistro: volviendo a VistaLogin.")
        self.login_window = Login()
        self.login_window.show()
        self.close()