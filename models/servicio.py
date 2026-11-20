"""Servicios de Software FJ: salas, equipos y asesorías."""

from abc import ABC, abstractmethod
from math import isfinite

from exceptions.custom_exceptions import ServicioNoDisponibleError
from utils.logger import LoggerSistema


def error(mensaje, tipo=ValueError):
    """Guarda el error y lo comunica al programa."""
    LoggerSistema.registrar_evento(mensaje, "ERROR")
    raise tipo(mensaje)


def validar_texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        error(f"{campo} no puede estar vacío.")
    return valor.strip()


def validar_numero(valor, campo, permite_cero=False):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        error(f"{campo} debe ser un número.")
    try:
        valido = isfinite(valor)
    except OverflowError:
        valido = False
    if not valido or valor < 0 or (valor == 0 and not permite_cero):
        error(f"{campo} debe ser un número válido y no negativo" +
              ("." if permite_cero else ", mayor que cero."))
    return valor


class Servicio(ABC):
    """Base común para todos los servicios."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        self.nombre = validar_texto(nombre, "El nombre")
        self.tarifa_hora = validar_numero(tarifa_hora, "La tarifa")
        if not isinstance(disponible, bool):
            error("La disponibilidad debe ser True o False.")
        self.disponible = disponible

    def revisar_disponibilidad(self, duracion):
        validar_numero(duracion, "La duración")
        if not self.disponible:
            error(f"El servicio {self.nombre} no está disponible.",
                  ServicioNoDisponibleError)

    def total(self, subtotal, descuento, impuesto):
        validar_numero(subtotal, "El subtotal", permite_cero=True)
        validar_numero(descuento, "El descuento", permite_cero=True)
        validar_numero(impuesto, "El impuesto", permite_cero=True)
        if descuento > 100 or impuesto > 100:
            error("Descuento e impuesto deben estar entre 0 y 100.")

        precio = round(subtotal * (1 - descuento / 100) *
                       (1 + impuesto / 100), 2)
        validar_numero(precio, "El precio final", permite_cero=True)
        LoggerSistema.registrar_evento(f"Costo de {self.nombre}: {precio} COP")
        return precio

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            error("La capacidad debe ser un entero mayor que cero.")
        self.capacidad = capacidad
        LoggerSistema.registrar_evento(f"Sala creada: {self.nombre}")

    def validar_parametros(self, duracion):
        self.revisar_disponibilidad(duracion)
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        return self.total(self.tarifa_hora * duracion, descuento, impuesto)

    def describir(self):
        return f"Sala: {self.nombre}, capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, tipo_equipo,
                 costo_mantenimiento=0, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self.tipo_equipo = validar_texto(tipo_equipo, "El tipo de equipo")
        self.costo_mantenimiento = validar_numero(
            costo_mantenimiento, "El mantenimiento", permite_cero=True)
        LoggerSistema.registrar_evento(f"Equipo creado: {self.nombre}")

    def validar_parametros(self, duracion):
        self.revisar_disponibilidad(duracion)
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self.tarifa_hora * duracion + self.costo_mantenimiento
        return self.total(subtotal, descuento, impuesto)

    def describir(self):
        return f"Equipo: {self.nombre}, tipo: {self.tipo_equipo}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, tarifa_hora, especialidad,
                 costo_preparacion=0, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self.especialidad = validar_texto(especialidad, "La especialidad")
        self.costo_preparacion = validar_numero(
            costo_preparacion, "La preparación", permite_cero=True)
        LoggerSistema.registrar_evento(f"Asesoría creada: {self.nombre}")

    def validar_parametros(self, duracion):
        self.revisar_disponibilidad(duracion)
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self.tarifa_hora * duracion + self.costo_preparacion
        return self.total(subtotal, descuento, impuesto)

    def describir(self):
        return f"Asesoría: {self.nombre}, especialidad: {self.especialidad}"
