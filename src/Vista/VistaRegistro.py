from PyQt5.QtWidgets import QMainWindow, QMessageBox # Importamos QMessageBox
from PyQt5 import uic
from datetime import date # Importamos date para trabajar con fechas


# Importa la vista de Login para poder navegar de vuelta a ella
from src.Vista.Login import Login


Form_Registro, Window_Registro = uic.loadUiType("./src/Vista/Ui/VistaRegistro.ui")

class VistaRegistro(QMainWindow, Form_Registro):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets de VistaRegistro

        # Conectar el botón 'btn_registrar'
        self.btn_registrar.clicked.connect(self.procesar_registro)

        # Conectar el botón 'btn_volver_login' (si lo añadiste en el .ui)
        self.btn_volver_login.clicked.connect(self.volver_a_login)

        # Para mantener una referencia a la ventana de login
        self.login_window = None

        # Configurar QDateEdit para que no permita fechas futuras (opcional, pero buena práctica)
        # self.dateedit_fecha_nacimiento.setMaximumDate(date.today())

    def procesar_registro(self):
        """
        Función para manejar el clic del botón de registro.
        Obtiene los datos de los campos y simula un registro.
        Navega a la ventana de login SOLO SI EL REGISTRO ES EXITOSO.
        """
        # --- Campos OBLIGATORIOS (según tu esquema de DB) ---
        nombre = self.txt_nombre.text().strip()
        apellidos = self.txt_apellidos.text().strip()
        email = self.txt_email.text().strip()
        contrasena = self.txt_password.text()
        confirm_contrasena = self.txt_confirm_password.text()

        # --- Campos NO OBLIGATORIOS (según tu esquema de DB, o condicionales) ---
        # QDateEdit.date() retorna un objeto QDate, lo convertimos a string 'YYYY-MM-DD'
        fecha_nacimiento_qdate = self.dateedit_fecha_nacimiento.date()
        fecha_nacimiento = fecha_nacimiento_qdate.toString("yyyy-MM-dd") if fecha_nacimiento_qdate.isValid() else None

        telefono = self.txt_telefono.text().strip()
        peso_corporal = self.spinbox_peso_corporal.value() if self.spinbox_peso_corporal.value() > 0 else None
        # Si peso_corporal fuera obligatorio para el rol 'Atleta' en este punto,
        # la validación sería más compleja (después de elegir el rol o asumir el rol inicial)


        print(f"Intento de registro con todos los datos:")
        print(f"  Nombre: {nombre}")
        print(f"  Apellidos: {apellidos}")
        print(f"  Email: {email}")
        print(f"  Contraseña: {'*' * len(contrasena)}") # No imprimir contraseña real en consola
        print(f"  Fecha Nacimiento: {fecha_nacimiento}")
        print(f"  Teléfono: {telefono}")
        print(f"  Peso Corporal: {peso_corporal} kg")

        # --- Lógica de Validación ---
        errores = []

        # Validación de campos obligatorios
        if not nombre:
            errores.append("El Nombre es obligatorio.")
        if not apellidos:
            errores.append("Los Apellidos son obligatorios.")
        if not email:
            errores.append("El Correo Electrónico es obligatorio.")
        if not contrasena:
            errores.append("La Contraseña es obligatoria.")
        if not confirm_contrasena:
            errores.append("La Confirmación de Contraseña es obligatoria.")

        # Validaciones de formato y coincidencia
        if contrasena != confirm_contrasena:
            errores.append("Las contraseñas no coinciden.")
        
        if "@" not in email or "." not in email:
            errores.append("El formato del Correo Electrónico no es válido.")

        # Mostrar errores si los hay
        if errores:
            QMessageBox.warning(self, "Error de Registro", "\n".join(errores))
            return

        # --- SIMULACIÓN DE REGISTRO EXITOSO ---
        # En un caso real, aquí llamarías a tu capa del Modelo/DAO para guardar el usuario en la DB.
        # Asumiremos que por defecto, el usuario que se registra es un 'Atleta'.
        rol_por_defecto = 'Atleta'

        # Ejemplo de cómo podrías llamar a tu DAO (pseudocódigo)
        # from src.Modelo.VO.UsuarioVO import UsuarioVO # Si tienes un Value Object para Usuario
        # from src.Modelo.DAO.UsuarioDAO import UsuarioDAO
        # try:
        #     nuevo_usuario_vo = UsuarioVO(
        #         id_usuario=None, # La DB lo genera
        #         nombre=nombre,
        #         apellidos=apellidos,
        #         email=email,
        #         contrasena=contrasena, # ¡RECORDATORIO: HASHEAR LA CONTRASEÑA ANTES DE GUARDARLA EN LA DB!
        #         rol=rol_por_defecto,
        #         fecha_registro=None, # La DB lo genera
        #         fecha_nacimiento=fecha_nacimiento,
        #         telefono=telefono,
        #         peso_corporal=peso_corporal
        #     )
        #     usuario_dao = UsuarioDAO()
        #     usuario_dao.registrar_usuario(nuevo_usuario_vo) # O pasar los campos directamente
        #     QMessageBox.information(self, "Registro Exitoso", "¡Usuario registrado correctamente! Ahora puede iniciar sesión.")
        #     self.volver_a_login() # Navegar a la pantalla de login tras el éxito
        # except Exception as e:
        #     QMessageBox.critical(self, "Error de Registro", f"No se pudo registrar el usuario: {e}. Por favor, inténtelo de nuevo.")
        #     # Puedes limpiar campos de contraseña si quieres
        #     self.txt_password.clear()
        #     self.txt_confirm_password.clear()

        # Si todo es válido y la simulación es exitosa:
        QMessageBox.information(self, "Registro Exitoso", "¡Usuario registrado correctamente (simulado)! Ahora puede iniciar sesión.")
        self.volver_a_login() # Navegar a la pantalla de login SOLO si el registro es exitoso

    def volver_a_login(self):
        """
        Función para cerrar esta ventana y abrir la ventana de Login.
        """
        print("Volviendo a la pantalla de Login...")
        from src.Vista.Login import Login # Importar aquí para evitar importaciones circulares si es necesario
        self.login_window = Login()  # Crea una instancia de la ventana de Login
        self.login_window.show()     # Muestra la ventana de Login
        self.close()                 # Cierra la ventana actual (VistaRegistro)