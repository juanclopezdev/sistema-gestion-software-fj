"""Modelo de reserva del sistema Software FJ."""

import math

from exceptions.custom_exceptions import (
    ClienteInvalidoError,
    ReservaError,
    ServicioNoDisponibleError,
)
from models.cliente import Cliente
from models.entidad import Entidad
from models.servicio import (
    AlquilerEquipo,
    AsesoriaEspecializada,
    ReservaSala,
)
from utils.logger import LoggerSistema


class Reserva(Entidad):
    """Integra cliente, servicio, duración y estado de una reserva."""

    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA"}

    TIPOS_SERVICIO = (
        ReservaSala,
        AlquilerEquipo,
        AsesoriaEspecializada,
    )

    def __init__(
        self,
        id_reserva,
        cliente,
        servicio,
        duracion_horas,
        descuento=0,
        impuesto=0,
    ):
        try:
            super().__init__(id_reserva)

            self.id_reserva = self.id_entidad
            self.cliente = cliente
            self.servicio = servicio
            self.duracion_horas = duracion_horas
            self.descuento = descuento
            self.impuesto = impuesto
            self.estado = "PENDIENTE"
            self.monto_total = 0.0

            self.validar()

        except Exception as exc:
            LoggerSistema.registrar_evento(
                f"Error al crear la reserva {id_reserva!r}: {exc}",
                "ERROR",
            )
            if isinstance(exc, ReservaError):
                raise
            raise ReservaError(
                f"No se pudo crear la reserva {id_reserva!r}."
            ) from exc

    def validar(self):
        """Valida los datos básicos de la reserva."""
        if not self.id_reserva:
            raise ReservaError("El identificador de la reserva es obligatorio.")

        if not isinstance(self.cliente, Cliente):
            raise ReservaError("La reserva debe tener un cliente válido.")

        if not isinstance(self.servicio, self.TIPOS_SERVICIO):
            raise ReservaError("El servicio asignado a la reserva no es válido.")

        if (
            isinstance(self.duracion_horas, bool)
            or not isinstance(self.duracion_horas, (int, float))
            or not math.isfinite(self.duracion_horas)
        ):
            raise ReservaError("La duración debe ser un número válido.")

        if self.estado not in self.ESTADOS_VALIDOS:
            raise ReservaError(f"El estado {self.estado!r} no es válido.")

        return True

    def obtener_resumen(self):
        """Devuelve un resumen legible de la reserva."""
        return (
            f"Reserva [{self.id_reserva}] - "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion_horas} horas | "
            f"Estado: {self.estado} | "
            f"Total: {self.monto_total} COP"
        )

    def procesar(self):
        """Valida cliente y servicio, calcula el costo y confirma la reserva."""
        try:
            self.validar()

            if self.estado != "PENDIENTE":
                raise ReservaError(
                    f"La reserva '{self.id_reserva}' no está pendiente."
                )

            self.cliente.validar()

            monto = self.servicio.calcular_costo(
                self.duracion_horas,
                descuento=self.descuento,
                impuesto=self.impuesto,
            )

            if (
                isinstance(monto, bool)
                or not isinstance(monto, (int, float))
                or not math.isfinite(monto)
                or monto < 0
            ):
                raise ValueError("El servicio devolvió un costo inválido.")

        except ServicioNoDisponibleError as exc:
            self.estado = "CANCELADA"
            LoggerSistema.registrar_evento(
                f"Error al procesar reserva '{self.id_reserva}': "
                f"servicio no disponible. Causa: {exc}",
                "ERROR",
            )
            raise ReservaError(
                f"No se pudo confirmar la reserva '{self.id_reserva}': "
                "servicio no disponible."
            ) from exc

        except (ValueError, ClienteInvalidoError) as exc:
            self.estado = "CANCELADA"
            LoggerSistema.registrar_evento(
                f"Error al procesar reserva '{self.id_reserva}': "
                f"datos o parámetros inválidos. Causa: {exc}",
                "ERROR",
            )
            raise ReservaError(
                f"No se pudo confirmar la reserva '{self.id_reserva}': "
                "datos o parámetros inválidos."
            ) from exc

        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Error de reserva '{self.id_reserva}': {exc}",
                "ERROR",
            )
            raise

        except Exception as exc:
            LoggerSistema.registrar_evento(
                f"Error inesperado en reserva '{self.id_reserva}': {exc}",
                "ERROR",
            )
            raise ReservaError(
                f"Ocurrió un error al procesar la reserva '{self.id_reserva}'."
            ) from exc

        else:
            self.monto_total = float(monto)
            self.estado = "CONFIRMADA"

            LoggerSistema.registrar_evento(
                f"Reserva '{self.id_reserva}' confirmada por "
                f"{self.monto_total} COP.",
                "INFO",
            )
            return self.monto_total

        finally:
            LoggerSistema.registrar_evento(
                f"Finalizó el intento de procesar la reserva "
                f"'{self.id_reserva}'.",
                "INFO",
            )

    def confirmar(self):
        """Confirma la reserva procesando el costo del servicio."""
        return self.procesar()

    def cancelar(self, motivo="Cancelación solicitada"):
        """Cancela la reserva y registra el motivo."""
        try:
            self.validar()

            if self.estado == "CANCELADA":
                raise ReservaError(
                    f"La reserva '{self.id_reserva}' ya se encuentra cancelada."
                )

            self.estado = "CANCELADA"

        except ReservaError as exc:
            LoggerSistema.registrar_evento(
                f"Error al cancelar la reserva '{self.id_reserva}': {exc}",
                "ERROR",
            )
            raise

        except Exception as exc:
            LoggerSistema.registrar_evento(
                f"Error inesperado al cancelar la reserva "
                f"'{self.id_reserva}': {exc}",
                "ERROR",
            )
            raise ReservaError(
                f"No se pudo cancelar la reserva '{self.id_reserva}'."
            ) from exc

        else:
            LoggerSistema.registrar_evento(
                f"Reserva '{self.id_reserva}' cancelada. Motivo: {motivo}",
                "INFO",
            )

        finally:
            LoggerSistema.registrar_evento(
                f"Finalizó el intento de cancelar la reserva "
                f"'{self.id_reserva}'.",
                "INFO",
            )