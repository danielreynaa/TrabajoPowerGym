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

        self.btn_registrar.clicked.connect(self.procesar_registro)
        self.btn_volver_login.clicked.connect(self.volver_a_login)
        self.login_window = None

        self.logger = CustomLogger() 
        self.logger.info("Vista Registro cargada.") 

    def procesar_registro(self):
        nombre = self.txt_nombre.text().strip()
        apellidos = self.txt_apellidos.text().strip()
        email = self.txt_email.text().strip()
        contrasena = self.txt_password.text()
        confirm_contrasena = self.txt_confirm_password.text()
        rol = self.combo_rol.currentText().strip() 

        fecha_nacimiento_qdate = self.dateedit_fecha_nacimiento.date()
        fecha_nacimiento = (
            fecha_nacimiento_qdate.toString("yyyy-MM-dd")
            if fecha_nacimiento_qdate.isValid()
            else None
        )
        telefono = self.txt_telefono.text().strip()
        peso_corporal = (
            self.spinbox_peso_corporal.value()
            if self.spinbox_peso_corporal.value() > 0
            else None
        )

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
        if not rol:
            errores.append("Debe seleccionar un tipo de usuario.")

        if errores:
            self.logger.warning(f"Errores de validación en el registro para {email}: {', '.join(errores)}")
            QMessageBox.warning(self, "Error de Registro", "\n".join(errores))
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        user_bo = UserBO()

        try:
            user_bo.registrar_usuario(
                nombre=nombre,
                apellidos=apellidos,
                email=email,
                contrasena=contrasena_hash,
                rol=rol, 
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                peso_corporal=peso_corporal,
            )
            self.logger.info(f"Nuevo usuario {email} registrado exitosamente con rol: {rol}.")
            QMessageBox.information(
                self,
                "Registro Exitoso",
                "¡Usuario registrado correctamente! Ahora puede iniciar sesión.",
            )
            self.volver_a_login()

        except Exception as e:
            self.logger.error(f"Fallo al registrar usuario {email}: {e}")
            QMessageBox.critical(
                self, "Error de Registro", f"No se pudo registrar el usuario: {e}"
            )
            self.txt_password.clear()
            self.txt_confirm_password.clear()

    def volver_a_login(self):
        self.logger.info("Volviendo de VistaRegistro a VistaLogin (botón 'Volver').")
        self.login_window = Login()
        self.login_window.show()
        self.close()