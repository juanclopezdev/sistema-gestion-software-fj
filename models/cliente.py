"""Módulo que define la clase Cliente con encapsulación y validaciones estrictas."""

import re
from exceptions.custom_exceptions import ClienteInvalidoError
from models.entidad import Entidad


class Cliente(Entidad):
    """Representa a un cliente registrado en Software FJ."""

    def __init__(
        self,
        id_cliente: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
    ) -> None:
        """Inicializa y valida un nuevo cliente del sistema.

        Args:
            id_cliente (str): Identificador interno del cliente.
            nombre (str): Nombre completo del cliente.
            documento (str): Número de identificación del cliente.
            correo (str): Correo electrónico de contacto.
            telefono (str): Número telefónico de contacto.

        Raises:
            ClienteInvalidoError: Si algún dato personal es inválido o incompleto.
        """
        super().__init__(id_cliente)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.validar()

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre completo del cliente."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre del cliente debe ser un texto de al menos 3 caracteres."
            )
        self._nombre = valor.strip()

    @property
    def documento(self) -> str:
        """Obtiene el documento de identidad del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Valida que el documento contenga entre 6 y 15 dígitos numéricos."""
        if not isinstance(valor, str) or not re.fullmatch(r"\d{6,15}", valor.strip()):
            raise ClienteInvalidoError(
                f"Documento inválido ('{valor}'). Debe contener entre 6 y 15 dígitos numéricos."
            )
        self._documento = valor.strip()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato básico del correo electrónico."""
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not isinstance(valor, str) or not re.match(patron_correo, valor.strip()):
            raise ClienteInvalidoError(
                f"Correo electrónico inválido ('{valor}')."
            )
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Obtiene el número de teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga entre 7 y 15 dígitos."""
        if not isinstance(valor, str) or not re.fullmatch(r"\d{7,15}", valor.strip()):
            raise ClienteInvalidoError(
                f"Teléfono inválido ('{valor}'). Debe contener entre 7 y 15 dígitos."
            )
        self._telefono = valor.strip()

    def validar(self) -> bool:
        """Verifica que el ID del cliente sea válido."""
        if not self._id_entidad:
            raise ClienteInvalidoError("El ID del cliente no puede estar vacío.")
        return True

    def obtener_resumen(self) -> str:
        """Retorna una cadena legible con la información del cliente."""
        return (
            f"Cliente [{self.id_entidad}] - {self.nombre} | "
            f"Doc: {self.documento} | Correo: {self.correo} | Tel: {self.telefono}"
        )
