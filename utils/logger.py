import datetime

class LoggerSistema:
    _archivo_log = "sistema_log.txt"

    @classmethod
    def registrar_evento(cls, mensaje: str, tipo: str = "INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{tipo}] {mensaje}\n"
        try:
            with open(cls._archivo_log, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error crítico al escribir en el archivo de log: {e}")
