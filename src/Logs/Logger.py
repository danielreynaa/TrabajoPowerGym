
import os
from datetime import datetime

class CustomLogger:
    _instance = None
    _initialized = False 

    def __new__(cls, log_file="app.log", log_level="INFO"):
        if cls._instance is None:
            print(f"DEBUG: Creando la única instancia de CustomLogger para '{log_file}'...")
            cls._instance = super(CustomLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file="app.log", log_level="INFO"):
        if not CustomLogger._initialized:
            print(f"DEBUG: Inicializando CustomLogger con archivo '{log_file}' y nivel '{log_level}'.")
            self.log_file = log_file
            self.log_level = log_level.upper()
            self._setup_logger()
            CustomLogger._initialized = True
        else:
            pass 

    def _setup_logger(self):
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def _write_log(self, level, message):
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