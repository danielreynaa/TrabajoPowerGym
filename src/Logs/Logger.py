# C:\Users\elded\OneDrive\Escritorio\INGENIERÍA DE SOFTWARE\POWER GYM\TrabajoPowerGym\src\Logs\Logger.py

import os
from datetime import datetime

class CustomLogger:
    _instance = None
    _initialized = False # Para asegurar que la inicialización solo ocurra una vez

    def __new__(cls, log_file="app.log", log_level="INFO"):
        if cls._instance is None:
            print(f"DEBUG: Creando la única instancia de CustomLogger para '{log_file}'...")
            cls._instance = super(CustomLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file="app.log", log_level="INFO"):
        # Solo inicializa la primera vez que se crea la instancia lógica
        if not CustomLogger._initialized:
            print(f"DEBUG: Inicializando CustomLogger con archivo '{log_file}' y nivel '{log_level}'.")
            self.log_file = log_file
            self.log_level = log_level.upper()
            self._setup_logger()
            CustomLogger._initialized = True
        else:
            pass # Instancia ya inicializada, ignorar parámetros en llamadas subsecuentes.

    def _setup_logger(self):
        """Configura el archivo de log y el nivel."""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def _write_log(self, level, message):
        """Escribe un mensaje en el archivo de log y lo imprime en consola."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message)
            print(f"LOG: {log_message.strip()}") 
        except IOError as e:
            print(f"ERROR: No se pudo escribir en el archivo de log {self.log_file}: {e}")

    def debug(self, message):
        if self.log_level == "DEBUG":
            self._write_log("DEBUG", message)

    def info(self, message):
        if self.log_level in ["DEBUG", "INFO"]:
            self._write_log("INFO", message)

    def warning(self, message):
        if self.log_level in ["DEBUG", "INFO", "WARNING"]:
            self._write_log("WARNING", message)

    def error(self, message):
        if self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            self._write_log("ERROR", message)

    def critical(self, message):
        if self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            self._write_log("CRITICAL", message)