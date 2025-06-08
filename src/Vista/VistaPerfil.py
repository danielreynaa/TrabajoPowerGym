# src/Vista/VistaPerfil.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import hashlib
from datetime import datetime

from src.controlador.ControladorUser import ControladorUser
from src.Logs.Logger import CustomLogger
from src.Modelo.VO.SuperVo import SuperVo

Form, _ = uic.loadUiType("src/Vista/Ui/VistaPerfil.ui")

class VistaPerfil(QMainWindow, Form):
    def __init__(self, usuario_email, volver_callback):
        super().__init__()
        self.setupUi(self)

        self.usuario_email   = usuario_email
        self.volver_callback = volver_callback

        self.controller = ControladorUser()
        self.logger     = CustomLogger()
        self.logger.info(f"VistaPerfil cargada para {usuario_email}")

        # Carga datos al iniciar
        self._cargar_datos()

        # Conectar botones (asegúrate de que btn_guardar y btn_volver existan en el .ui)
        self.btn_guardar.clicked.connect(self._guardar_cambios)
        self.btn_volver.clicked.connect(self._volver_al_menu)

    def _cargar_datos(self):
        vo: SuperVo = self.controller.obtener_usuario_por_email(self.usuario_email)
        if not vo:
            QMessageBox.critical(self, "Error", "No se encontró el perfil del usuario.")
            self.close()
            return

        self.inputNombre.setText(vo.nombre)
        self.inputApellidos.setText(vo.apellidos)
        self.inputEmail.setText(vo.email)
        # Mostrar el hash; si prefieres la contraseña en texto claro, omite esto
        self.inputContrasena.setText(vo.contrasena)

        if vo.fecha_nacimiento:
            # vo.fecha_nacimiento podría ser string "YYYY-MM-DD" o QDate
            try:
                fecha = datetime.strptime(vo.fecha_nacimiento, "%Y-%m-%d")
                self.inpuFechaDeNacimiento.setDate(fecha)
            except Exception:
                pass

        self.inputTelefono.setText(vo.telefono or "")
        self.inputPeso.setValue(vo.peso_corporal or 0.0)

    def _guardar_cambios(self):
        # Recolectar los datos del formulario
        nombre   = self.inputNombre.text().strip()
        apellidos= self.inputApellidos.text().strip()
        email    = self.inputEmail.text().strip()
        passwd   = self.inputContrasena.text().strip()

        # Hash de contraseña
        contrasena_hash = hashlib.sha256(passwd.encode()).hexdigest()

        fecha_qdate = self.inpuFechaDeNacimiento.date()
        fecha_nac   = fecha_qdate.toString("yyyy-MM-dd")

        telefono = self.inputTelefono.text().strip()
        peso     = self.inputPeso.value()

        # Crear el VO
        vo = SuperVo(
            id_usuario       = None,
            nombre           = nombre,
            apellidos        = apellidos,
            email            = email,
            contrasena       = contrasena_hash,
            rol              = None,
            fecha_registro   = None,
            fecha_nacimiento = fecha_nac,
            telefono         = telefono,
            peso_corporal    = peso
        )

        # Opción A: BO lanza excepción si falla
        try:
            self.controller.actualizar_usuario(vo)
            QMessageBox.information(self, "Perfil actualizado", "Los datos se guardaron correctamente.")
            self.logger.info(f"Perfil de {email} actualizado con éxito")
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", str(e))
            self.logger.error(f"Error al actualizar perfil de {email}: {e}")

    def _volver_al_menu(self):
        if self.volver_callback:
            self.close()
            self.volver_callback()
