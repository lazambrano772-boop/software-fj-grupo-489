"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
"""
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)
from logger_config import obtener_logger

logger = obtener_logger()


def _es_numero(valor):
    """True si es int o float (los booleanos no cuentan como número)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(EntidadBase, ABC):
    """Clase abstracta de la que heredan todos los servicios de Software FJ."""

    IVA_DEFECTO = 0.19
    DESCUENTO_MAXIMO = 0.50
    _secuencia = 0

    def __init__(self, nombre, tarifa_hora):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        if not _es_numero(tarifa_hora) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: '{tarifa_hora}'. Debe ser mayor que 0.")

        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True
        Servicio._secuencia += 1
        super().__init__(f"SRV-{Servicio._secuencia:03d}")
        logger.info(f"Servicio creado: {self.id} - {self._nombre} ({type(self).__name__})")

    # ---- propiedades (encapsulación) ----
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def habilitar(self):
        self._disponible = True
        logger.info(f"Servicio {self.id} habilitado.")

    def deshabilitar(self):
        self._disponible = False
        logger.warning(f"Servicio {self.id} marcado como NO disponible.")

    # ---- métodos abstractos: cada servicio los sobrescribe ----
    @abstractmethod
    def validar_parametros(self, horas):
        """Valida la duración solicitada según las reglas del servicio."""

    @abstractmethod
    def calcular_costo(self, horas, **opciones):
        """Costo base (sin impuestos ni descuentos)."""

    @abstractmethod
    def describir(self):
        """Descripción del servicio."""

    @staticmethod
    def _validar_horas(horas, minimo, maximo):
        """Validación común de la duración."""
        if horas is None:
            raise ParametroFaltanteError("Debe indicar la duración (horas) del servicio.")
        if not _es_numero(horas) or horas <= 0:
            raise ServicioInvalidoError(f"Duración inválida: '{horas}'. Debe ser un número positivo.")
        if not minimo <= horas <= maximo:
            raise ServicioInvalidoError(f"Duración fuera de rango: {horas} h (permitido {minimo}-{maximo} h).")

    # ---- SOBRECARGA SIMULADA del cálculo de costos ----
    def costo_total(self, horas, impuesto=None, descuento=None, **opciones):
        """
        Python no tiene sobrecarga nativa; se simula con parámetros opcionales.
        Variantes:
          costo_total(h)                    -> con IVA por defecto
          costo_total(h, 0.08)              -> con impuesto personalizado
          costo_total(h, 0.19, 0.10)        -> con impuesto y descuento
          costo_total(h, descuento=0.10)    -> solo descuento
          costo_total(h, con_catering=True) -> opciones propias de cada servicio
        """
        if impuesto is None:
            impuesto = self.IVA_DEFECTO
        if descuento is None:
            descuento = 0.0

        if not _es_numero(impuesto) or not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto inconsistente: {impuesto} (debe estar entre 0 y 1).")
        if not _es_numero(descuento) or not 0 <= descuento <= self.DESCUENTO_MAXIMO:
            raise CalculoInconsistenteError(
                f"Descuento inconsistente: {descuento} (máximo {self.DESCUENTO_MAXIMO}).")

        base = self.calcular_costo(horas, **opciones)
        if base <= 0:
            raise CalculoInconsistenteError(f"El costo base calculado es inválido: {base}.")

        return round(base * (1 - descuento) * (1 + impuesto), 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones o capacitación."""

    COSTO_CATERING_HORA = 20000

    def __init__(self, nombre, tarifa_hora, capacidad):
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or not 1 <= capacidad <= 200:
            raise ServicioInvalidoError(f"Capacidad inválida: '{capacidad}' (permitido 1-200 personas).")
        self.__capacidad = capacidad
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 12)

    def calcular_costo(self, horas, con_catering=False):
        self.validar_parametros(horas)

        # Validar que la opción de catering sea correcta
        if not isinstance(con_catering, bool):
            raise ServicioInvalidoError("La opción de catering debe ser True o False.")

        costo = self._tarifa_hora * horas
        if self.__capacidad > 50:
            costo *= 1.10
        if con_catering:
            costo += self.COSTO_CATERING_HORA * horas

        return round(costo, 2)

    def describir(self):
        return f"Sala '{self._nombre}' | capacidad {self.__capacidad} | ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, cantidad=1):
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or not 1 <= cantidad <= 20:
            raise ServicioInvalidoError(f"Cantidad inválida: '{cantidad}' (permitido 1-20).")

        self.__tipo_equipo = tipo_equipo.strip()
        self.__cantidad = cantidad
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 72)

    def calcular_costo(self, horas, cantidad=None):
        self.validar_parametros(horas)
        unidades = self.__cantidad if cantidad is None else cantidad

        # Validar la cantidad de equipos solicitada
        if (not isinstance(unidades, int) or isinstance(unidades, bool)
                or not 1 <= unidades <= 20):
            raise CalculoInconsistenteError(
                f"Cantidad de equipos inconsistente: {unidades} (permitido 1-20)."
            )

        return round(self._tarifa_hora * horas * unidades, 2)

    def describir(self):
        return (f"Equipo '{self._nombre}' ({self.__tipo_equipo}) x{self.__cantidad} | "
                f"${self._tarifa_hora:,.0f}/h por unidad")


class AsesoriaEspecializada(Servicio):
    """Asesorías con consultores según su nivel de experiencia."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad de la asesoría es obligatoria.")
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido '{nivel}'. Opciones: {', '.join(self.NIVELES)}.")

        self.__especialidad = especialidad.strip()
        self.__nivel = nivel.lower()
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self, horas):
        self._validar_horas(horas, 1, 8)

    def calcular_costo(self, horas, urgente=False):
        self.validar_parametros(horas)

        # Validar que la opción de urgencia sea correcta
        if not isinstance(urgente, bool):
            raise ServicioInvalidoError("La opción de urgencia debe ser True o False.")

        costo = self._tarifa_hora * horas * self.NIVELES[self.__nivel]
        if urgente:
            costo *= 1.25

        return round(costo, 2)

    def describir(self):
        return (f"Asesoría '{self._nombre}' ({self.__especialidad}, nivel {self.__nivel}) | "
                f"${self._tarifa_hora:,.0f}/h")


    
