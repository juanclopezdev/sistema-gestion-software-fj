"""Módulo que define la clase abstracta base Entidad para el sistema Software FJ."""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta base que representa una entidad general del sistema."""

    def __init__(self, id_entidad: str) -> None:
        """Inicializa los atributos comunes de toda entidad.

        Args:
            id_entidad (str): Identificador único de la entidad.
        """
        self._id_entidad = id_entidad.strip() if isinstance(id_entidad, str) else ""
        self._fecha_registro = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Obtiene el identificador único de la entidad."""
        return self._id_entidad

    @property
    def fecha_registro(self) -> datetime:
        """Obtiene la fecha y hora en que fue registrada la entidad."""
        return self._fecha_registro

    @abstractmethod
    def validar(self) -> bool:
        """Valida la integridad de los datos de la entidad."""
        raise NotImplementedError

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una descripción resumida de la entidad."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Representación en cadena de texto de la entidad."""
        return self.obtener_resumen()
