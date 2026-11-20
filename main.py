"""Script principal de simulación para el Sistema Integral de Software FJ.

Ejecuta al menos 10 operaciones completas (clientes válidos e inválidos,
servicios correctos e incorrectos y reservas exitosas y fallidas) utilizando
manejo avanzado de excepciones y registro de eventos/errores en archivo de log
sin interrumpir la ejecución del sistema.
"""

from exceptions.custom_exceptions import (
    ClienteInvalidoError,
    ReservaError,
    ServicioNoDisponibleError,
)
from models.cliente import Cliente
from models.servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from utils.logger import LoggerSistema


class SimulacionReserva:
    """Gestiona una reserva en memoria integrando cliente, servicio y estado."""

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio,
        duracion_horas: float,
        descuento: float = 0,
        impuesto: float = 0,
    ) -> None:
        """Inicializa y valida los componentes básicos de una reserva."""
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.descuento = descuento
        self.impuesto = impuesto
        self.estado = "PENDIENTE"
        self.monto_total = 0.0

    def procesar(self) -> float:
        """Calcula el costo y confirma la reserva o lanza ReservaError."""
        try:
            self.cliente.validar()
            # Encadenamos excepciones para contextualizar el fallo dentro de la reserva.
            monto = self.servicio.calcular_costo(
                self.duracion_horas,
                descuento=self.descuento,
                impuesto=self.impuesto,
            )
        except ServicioNoDisponibleError as exc:
            self.estado = "CANCELADA"
            raise ReservaError(
                f"No se pudo confirmar la reserva '{self.id_reserva}': servicio no disponible."
            ) from exc
        except (ValueError, ClienteInvalidoError) as exc:
            self.estado = "CANCELADA"
            raise ReservaError(
                f"No se pudo confirmar la reserva '{self.id_reserva}': datos o parámetros inválidos."
            ) from exc
        else:
            self.monto_total = monto
            self.estado = "CONFIRMADA"
            return self.monto_total

    def cancelar(self, motivo: str = "Cancelación solicitada") -> None:
        """Cancela la reserva si no está ya cancelada."""
        if self.estado == "CANCELADA":
            raise ReservaError(f"La reserva '{self.id_reserva}' ya se encuentra cancelada.")
        self.estado = "CANCELADA"
        LoggerSistema.registrar_evento(
            f"Reserva '{self.id_reserva}' cancelada. Motivo: {motivo}", "INFO"
        )


def ejecutar_simulacion() -> None:
    """Ejecuta 12 operaciones completas para validar estabilidad y logs."""
    LoggerSistema.registrar_evento("Inicio de simulación Fase 4 - Software FJ", "INFO")

    clientes_registrados: list[Cliente] = []
    servicios_registrados: list = []
    reservas_registradas: list[SimulacionReserva] = []

    # --- OPERACIÓN 1: Registro válido de cliente (try / except / else / finally) ---
    try:
        cliente_1 = Cliente(
            id_cliente="CLI-001",
            nombre="Ana María Gómez",
            documento="1098765432",
            correo="ana.gomez@correo.com",
            telefono="3104567890",
        )
    except ClienteInvalidoError as exc:
        LoggerSistema.registrar_evento(f"Op 1 fallida (cliente): {exc}", "ERROR")
        print(f"[Op 1] Error al registrar cliente 1: {exc}")
    else:
        clientes_registrados.append(cliente_1)
        LoggerSistema.registrar_evento(f"Op 1 exitosa: {cliente_1.obtener_resumen()}", "INFO")
        print(f"[Op 1] Cliente registrado: {cliente_1.obtener_resumen()}")
    finally:
        print("[Op 1] Bloque finally ejecutado.")

    # --- OPERACIÓN 2: Registro inválido de cliente (correo/documento erróneos) ---
    try:
        cliente_invalido = Cliente(
            id_cliente="CLI-002",
            nombre="Lu",
            documento="abc123",
            correo="correo_sin_arroba",
            telefono="12",
        )
    except ClienteInvalidoError as exc:
        LoggerSistema.registrar_evento(f"Op 2 error controlado (cliente inválido): {exc}", "ERROR")
        print(f"[Op 2] Error controlado al registrar cliente inválido: {exc}")
    else:
        clientes_registrados.append(cliente_invalido)
    finally:
        print("[Op 2] Bloque finally ejecutado.")

    # --- OPERACIÓN 3: Segundo cliente válido ---
    try:
        cliente_2 = Cliente(
            id_cliente="CLI-003",
            nombre="Carlos Andrés Pérez",
            documento="1144556677",
            correo="carlos.perez@empresa.co",
            telefono="3159876543",
        )
    except ClienteInvalidoError as exc:
        LoggerSistema.registrar_evento(f"Op 3 fallida (cliente): {exc}", "ERROR")
        print(f"[Op 3] Error al registrar cliente 2: {exc}")
    else:
        clientes_registrados.append(cliente_2)
        LoggerSistema.registrar_evento(f"Op 3 exitosa: {cliente_2.obtener_resumen()}", "INFO")
        print(f"[Op 3] Cliente registrado: {cliente_2.obtener_resumen()}")
    finally:
        print("[Op 3] Bloque finally ejecutado.")

    # --- OPERACIÓN 4: Creación correcta de servicios especializados ---
    try:
        sala_juntas = ReservaSala("Sala Ejecutiva A", 45000, 12, disponible=True)
        portatil_dev = AlquilerEquipo("Laptop Dev i7", 18000, "Computador", costo_mantenimiento=6000)
        asesoria_arq = AsesoriaEspecializada(
            "Arquitectura Cloud", 60000, "Nube y Microservicios", costo_preparacion=15000
        )
    except Exception as exc:
        LoggerSistema.registrar_evento(f"Op 4 fallida (creación servicios): {exc}", "ERROR")
        print(f"[Op 4] Error al crear servicios: {exc}")
    else:
        servicios_registrados.extend([sala_juntas, portatil_dev, asesoria_arq])
        LoggerSistema.registrar_evento("Op 4 exitosa: 3 servicios creados.", "INFO")
        print("[Op 4] Servicios creados:", [s.describir() for s in servicios_registrados])
    finally:
        print("[Op 4] Bloque finally ejecutado.")

    # --- OPERACIÓN 5: Creación incorrecta de servicio (capacidad inválida) ---
    try:
        sala_erronea = ReservaSala("Sala Invalida", 30000, -5)
    except ValueError as exc:
        LoggerSistema.registrar_evento(f"Op 5 error controlado (servicio inválido): {exc}", "ERROR")
        print(f"[Op 5] Error controlado al crear servicio inválido: {exc}")
    else:
        servicios_registrados.append(sala_erronea)
    finally:
        print("[Op 5] Bloque finally ejecutado.")

    # --- OPERACIÓN 6: Reserva exitosa de sala con descuento e impuesto ---
    if clientes_registrados and len(servicios_registrados) >= 1:
        try:
            reserva_1 = SimulacionReserva(
                "RES-001",
                clientes_registrados[0],
                servicios_registrados[0],
                duracion_horas=4,
                descuento=10,
                impuesto=19,
            )
            total_1 = reserva_1.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(f"Op 6 fallida: {exc} | Causa: {exc.__cause__}", "ERROR")
            print(f"[Op 6] Error en reserva 1: {exc}")
        else:
            reservas_registradas.append(reserva_1)
            LoggerSistema.registrar_evento(
                f"Op 6 exitosa: {reserva_1.id_reserva} confirmada por {total_1} COP.", "INFO"
            )
            print(f"[Op 6] Reserva {reserva_1.id_reserva} confirmada. Total: {total_1} COP")
        finally:
            print("[Op 6] Bloque finally ejecutado.")

    # --- OPERACIÓN 7: Reserva exitosa de alquiler de equipo ---
    if clientes_registrados and len(servicios_registrados) >= 2:
        try:
            reserva_2 = SimulacionReserva(
                "RES-002",
                clientes_registrados[0],
                servicios_registrados[1],
                duracion_horas=3,
            )
            total_2 = reserva_2.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(f"Op 7 fallida: {exc} | Causa: {exc.__cause__}", "ERROR")
            print(f"[Op 7] Error en reserva 2: {exc}")
        else:
            reservas_registradas.append(reserva_2)
            LoggerSistema.registrar_evento(
                f"Op 7 exitosa: {reserva_2.id_reserva} confirmada por {total_2} COP.", "INFO"
            )
            print(f"[Op 7] Reserva {reserva_2.id_reserva} confirmada. Total: {total_2} COP")
        finally:
            print("[Op 7] Bloque finally ejecutado.")

    # --- OPERACIÓN 8: Reserva exitosa de asesoría especializada ---
    if len(clientes_registrados) >= 2 and len(servicios_registrados) >= 3:
        try:
            reserva_3 = SimulacionReserva(
                "RES-003",
                clientes_registrados[1],
                servicios_registrados[2],
                duracion_horas=2,
                descuento=5,
            )
            total_3 = reserva_3.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(f"Op 8 fallida: {exc} | Causa: {exc.__cause__}", "ERROR")
            print(f"[Op 8] Error en reserva 3: {exc}")
        else:
            reservas_registradas.append(reserva_3)
            LoggerSistema.registrar_evento(
                f"Op 8 exitosa: {reserva_3.id_reserva} confirmada por {total_3} COP.", "INFO"
            )
            print(f"[Op 8] Reserva {reserva_3.id_reserva} confirmada. Total: {total_3} COP")
        finally:
            print("[Op 8] Bloque finally ejecutado.")

    # --- OPERACIÓN 9: Reserva fallida por servicio no disponible (encadenamiento) ---
    if clientes_registrados and len(servicios_registrados) >= 1:
        servicios_registrados[0].disponible = False
        try:
            reserva_fallida_disp = SimulacionReserva(
                "RES-004",
                clientes_registrados[0],
                servicios_registrados[0],
                duracion_horas=2,
            )
            reserva_fallida_disp.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Op 9 error controlado: {exc} -> Causa original: {exc.__cause__}", "ERROR"
            )
            print(f"[Op 9] Error controlado: {exc} (Causa: {exc.__cause__})")
        finally:
            servicios_registrados[0].disponible = True
            print("[Op 9] Bloque finally ejecutado (disponibilidad restaurada).")

    # --- OPERACIÓN 10: Reserva fallida por duración inválida (encadenamiento) ---
    if clientes_registrados and len(servicios_registrados) >= 2:
        try:
            reserva_fallida_dur = SimulacionReserva(
                "RES-005",
                clientes_registrados[0],
                servicios_registrados[1],
                duracion_horas=-3,
            )
            reserva_fallida_dur.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Op 10 error controlado: {exc} -> Causa original: {exc.__cause__}", "ERROR"
            )
            print(f"[Op 10] Error controlado: {exc} (Causa: {exc.__cause__})")
        finally:
            print("[Op 10] Bloque finally ejecutado.")

    # --- OPERACIÓN 11: Cancelación válida de una reserva confirmada ---
    if reservas_registradas:
        try:
            reservas_registradas[0].cancelar("Reprogramación del cliente")
        except ReservaError as exc:
            LoggerSistema.registrar_evento(f"Op 11 error en cancelación: {exc}", "ERROR")
            print(f"[Op 11] Error al cancelar: {exc}")
        else:
            print(f"[Op 11] Reserva {reservas_registradas[0].id_reserva} cancelada correctamente.")
        finally:
            print("[Op 11] Bloque finally ejecutado.")

    # --- OPERACIÓN 12: Intento inválido de cancelar una reserva ya cancelada ---
    if reservas_registradas:
        try:
            reservas_registradas[0].cancelar("Segundo intento de cancelación")
        except ReservaError as exc:
            LoggerSistema.registrar_evento(f"Op 12 error controlado (doble cancelación): {exc}", "ERROR")
            print(f"[Op 12] Error controlado al cancelar duplicado: {exc}")
        finally:
            print("[Op 12] Bloque finally ejecutado.")

    LoggerSistema.registrar_evento("Fin de simulación - Sistema estable sin interrupciones.", "INFO")
    print("\nSimulación de 12 operaciones finalizada. Revisa 'sistema_log.txt' para el historial.")


if __name__ == "__main__":
    ejecutar_simulacion()