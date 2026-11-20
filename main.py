"""Script principal de simulación para el Sistema Integral de Software FJ.

Integra los módulos de clientes, servicios y reservas con manejo avanzado de
excepciones y registro de eventos/errores en archivo de log sin interrumpir
la ejecución del programa.
"""

from exceptions.custom_exceptions import (
    ClienteInvalidoError,
    ReservaError,
)
from models.cliente import Cliente
from models.reserva import Reserva
from models.servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from utils.logger import LoggerSistema


def ejecutar_simulacion() -> None:
    """Ejecuta 12 operaciones completas para validar el sistema integrado."""
    LoggerSistema.registrar_evento(
        "Inicio de simulación integrada Fase 4 - Software FJ", "INFO"
    )

    clientes_registrados: list[Cliente] = []
    servicios_registrados: list = []
    reservas_registradas: list[Reserva] = []

    # --- OPERACIÓN 1: Registro válido de cliente ---
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
        LoggerSistema.registrar_evento(
            f"Op 1 exitosa: {cliente_1.obtener_resumen()}", "INFO"
        )
        print(f"[Op 1] Cliente registrado: {cliente_1.obtener_resumen()}")
    finally:
        print("[Op 1] Bloque finally ejecutado.")

    # --- OPERACIÓN 2: Registro inválido de cliente (datos erróneos) ---
    try:
        cliente_invalido = Cliente(
            id_cliente="CLI-002",
            nombre="Lu",
            documento="abc123",
            correo="correo_sin_arroba",
            telefono="12",
        )
    except ClienteInvalidoError as exc:
        LoggerSistema.registrar_evento(
            f"Op 2 error controlado (cliente inválido): {exc}", "ERROR"
        )
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
        LoggerSistema.registrar_evento(
            f"Op 3 exitosa: {cliente_2.obtener_resumen()}", "INFO"
        )
        print(f"[Op 3] Cliente registrado: {cliente_2.obtener_resumen()}")
    finally:
        print("[Op 3] Bloque finally ejecutado.")

    # --- OPERACIÓN 4: Creación correcta de los 3 tipos de servicios ---
    try:
        sala_juntas = ReservaSala("Sala Ejecutiva A", 45000, 12, disponible=True)
        portatil_dev = AlquilerEquipo(
            "Laptop Dev i7", 18000, "Computador", costo_mantenimiento=6000
        )
        asesoria_arq = AsesoriaEspecializada(
            "Arquitectura Cloud",
            60000,
            "Nube y Microservicios",
            costo_preparacion=15000,
        )
    except Exception as exc:
        LoggerSistema.registrar_evento(
            f"Op 4 fallida (creación servicios): {exc}", "ERROR"
        )
        print(f"[Op 4] Error al crear servicios: {exc}")
    else:
        servicios_registrados.extend([sala_juntas, portatil_dev, asesoria_arq])
        LoggerSistema.registrar_evento("Op 4 exitosa: 3 servicios creados.", "INFO")
        print(
            "[Op 4] Servicios creados:",
            [s.describir() for s in servicios_registrados],
        )
    finally:
        print("[Op 4] Bloque finally ejecutado.")

    # --- OPERACIÓN 5: Creación incorrecta de servicio (capacidad inválida) ---
    try:
        sala_erronea = ReservaSala("Sala Invalida", 30000, -5)
    except ValueError as exc:
        LoggerSistema.registrar_evento(
            f"Op 5 error controlado (servicio inválido): {exc}", "ERROR"
        )
        print(f"[Op 5] Error controlado al crear servicio inválido: {exc}")
    else:
        servicios_registrados.append(sala_erronea)
    finally:
        print("[Op 5] Bloque finally ejecutado.")

    # --- OPERACIÓN 6: Reserva exitosa de sala con descuento e impuesto ---
    if clientes_registrados and len(servicios_registrados) >= 1:
        try:
            reserva_1 = Reserva(
                id_reserva="RES-001",
                cliente=clientes_registrados[0],
                servicio=servicios_registrados[0],
                duracion_horas=4,
                descuento=10,
                impuesto=19,
            )
            total_1 = reserva_1.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Op 6 fallida: {exc} | Causa: {exc.__cause__}", "ERROR"
            )
            print(f"[Op 6] Error en reserva 1: {exc}")
        else:
            reservas_registradas.append(reserva_1)
            print(
                f"[Op 6] Reserva {reserva_1.id_reserva} confirmada. Total: {total_1} COP"
            )
        finally:
            print("[Op 6] Bloque finally ejecutado.")

    # --- OPERACIÓN 7: Reserva exitosa de alquiler de equipo ---
    if clientes_registrados and len(servicios_registrados) >= 2:
        try:
            reserva_2 = Reserva(
                id_reserva="RES-002",
                cliente=clientes_registrados[0],
                servicio=servicios_registrados[1],
                duracion_horas=3,
            )
            total_2 = reserva_2.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Op 7 fallida: {exc} | Causa: {exc.__cause__}", "ERROR"
            )
            print(f"[Op 7] Error en reserva 2: {exc}")
        else:
            reservas_registradas.append(reserva_2)
            print(
                f"[Op 7] Reserva {reserva_2.id_reserva} confirmada. Total: {total_2} COP"
            )
        finally:
            print("[Op 7] Bloque finally ejecutado.")

    # --- OPERACIÓN 8: Reserva exitosa de asesoría especializada ---
    if len(clientes_registrados) >= 2 and len(servicios_registrados) >= 3:
        try:
            reserva_3 = Reserva(
                id_reserva="RES-003",
                cliente=clientes_registrados[1],
                servicio=servicios_registrados[2],
                duracion_horas=2,
                descuento=5,
            )
            total_3 = reserva_3.procesar()
        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Op 8 fallida: {exc} | Causa: {exc.__cause__}", "ERROR"
            )
            print(f"[Op 8] Error en reserva 3: {exc}")
        else:
            reservas_registradas.append(reserva_3)
            print(
                f"[Op 8] Reserva {reserva_3.id_reserva} confirmada. Total: {total_3} COP"
            )
        finally:
            print("[Op 8] Bloque finally ejecutado.")

    # --- OPERACIÓN 9: Reserva fallida por servicio no disponible ---
    if clientes_registrados and len(servicios_registrados) >= 1:
        servicios_registrados[0].disponible = False
        try:
            reserva_fallida_disp = Reserva(
                id_reserva="RES-004",
                cliente=clientes_registrados[0],
                servicio=servicios_registrados[0],
                duracion_horas=2,
            )
            reserva_fallida_disp.procesar()
        except ReservaError as exc:
            print(f"[Op 9] Error controlado: {exc} (Causa: {exc.__cause__})")
        finally:
            servicios_registrados[0].disponible = True
            print("[Op 9] Bloque finally ejecutado (disponibilidad restaurada).")

    # --- OPERACIÓN 10: Reserva fallida por duración inválida ---
    if clientes_registrados and len(servicios_registrados) >= 2:
        try:
            reserva_fallida_dur = Reserva(
                id_reserva="RES-005",
                cliente=clientes_registrados[0],
                servicio=servicios_registrados[1],
                duracion_horas=-3,
            )
            reserva_fallida_dur.procesar()
        except ReservaError as exc:
            print(f"[Op 10] Error controlado: {exc} (Causa: {exc.__cause__})")
        finally:
            print("[Op 10] Bloque finally ejecutado.")

    # --- OPERACIÓN 11: Cancelación válida de una reserva confirmada ---
    if reservas_registradas:
        try:
            reservas_registradas[0].cancelar("Reprogramación del cliente")
        except ReservaError as exc:
            print(f"[Op 11] Error al cancelar: {exc}")
        else:
            print(
                f"[Op 11] Reserva {reservas_registradas[0].id_reserva} cancelada correctamente."
            )
        finally:
            print("[Op 11] Bloque finally ejecutado.")

    # --- OPERACIÓN 12: Intento inválido de cancelar una reserva ya cancelada ---
    if reservas_registradas:
        try:
            reservas_registradas[0].cancelar("Segundo intento de cancelación")
        except ReservaError as exc:
            print(f"[Op 12] Error controlado al cancelar duplicado: {exc}")
        finally:
            print("[Op 12] Bloque finally ejecutado.")

    LoggerSistema.registrar_evento(
        "Fin de simulación integrada - Sistema estable sin interrupciones.",
        "INFO",
    )
    print(
        "\nSimulación de 12 operaciones finalizada. Revisa 'sistema_log.txt' para el historial."
    )


if __name__ == "__main__":
    ejecutar_simulacion()