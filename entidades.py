"""
entidades.py
Clase abstracta EntidadBase y clase Cliente (con encapsulación y validaciones).
"""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError
from logger_config import obtener_logger

logger = obtener_logger()


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        self._id = identificador   # Identificador único (protegido)

    @property
    def id(self):
        """Solo lectura: el identificador no se puede modificar desde fuera."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (polimorfismo)."""

    def __str__(self):
        return self.describir()


class Cliente(EntidadBase):
    """Cliente de Software FJ. Los datos personales son privados y validados."""

    _secuencia = 0  # Contador para generar identificadores CLI-001, CLI-002...
    _LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
    _PATRON_NOMBRE = re.compile(rf"^[{_LETRAS}][{_LETRAS} '.-]{{2,59}}$")
    _PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre, documento, email, telefono):
        # Cada asignación pasa por su setter, que valida y lanza excepción si falla
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        # El id solo se genera si TODAS las validaciones pasaron
        Cliente._secuencia += 1
        super().__init__(f"CLI-{Cliente._secuencia:03d}")
        logger.info(f"Cliente registrado: {self.id} - {self.nombre}")

    # ---------------- nombre ----------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre es obligatorio y debe ser texto.")
        valor = " ".join(valor.split())  # Quita espacios sobrantes
        if not self._PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(
                f"Nombre inválido '{valor}': use solo letras (3 a 60 caracteres)."
            )
        self.__nombre = valor

    # --------------- documento --------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        texto = str(valor).strip() if valor is not None else ""
        if not texto.isdigit() or not 6 <= len(texto) <= 12:
            raise ClienteInvalidoError(
                f"Documento inválido '{texto}': debe tener entre 6 y 12 dígitos."
            )
        self.__documento = texto

    # ----------------- email ----------------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self.__email = valor.strip().lower()

    # --------------- teléfono ---------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip() if valor is not None else ""
        if not texto.isdigit() or not 7 <= len(texto) <= 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido '{texto}': debe tener entre 7 y 10 dígitos."
            )
        self.__telefono = texto

    def describir(self):
        return (f"Cliente {self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.email} | Tel: {self.telefono}")
