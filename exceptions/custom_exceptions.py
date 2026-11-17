class SistemaFjError(Exception):
    """Excepción base para todos los errores del sistema."""
    pass

class ClienteInvalidoError(SistemaFjError):
    """Se lanza cuando los datos de un cliente no son válidos o están incompletos."""
    pass

class ServicioNoDisponibleError(SistemaFjError):
    """Se lanza cuando el servicio solicitado no está disponible o no existe."""
    pass

class ReservaError(SistemaFjError):
    """Se lanza cuando ocurre un fallo en el proceso de creación o gestión de una reserva."""
    pass
