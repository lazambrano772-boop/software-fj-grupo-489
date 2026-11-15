"""
reservas.py
Clase Reserva: integra cliente, servicio, duración y estado.
"""
from enum import Enum

from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioNoDisponibleError,
                         SoftwareFJError)
from logger_config import obtener_logger
from servicios import Servicio

logger = obtener_logger()


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"
    FALLIDA = "Fallida"


class Reserva(EntidadBase):
    """Reserva de un servicio por un cliente."""

    _secuencia = 0

    def __init__(self, cliente, servicio, horas, impuesto=None, descuento=None, **opciones):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        try:
            servicio.validar_parametros(horas)
        except SoftwareFJError as e:
            # Encadenamiento: se conserva el error original como causa (__cause__)
            raise ReservaInvalidaError(f"Datos de reserva inválidos: {e.mensaje}") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._impuesto = impuesto
        self._descuento = descuento
        self._opciones = opciones
        self._estado = EstadoReserva.PENDIENTE
        self._costo = None
        Reserva._secuencia += 1
        super().__init__(f"RES-{Reserva._secuencia:03d}")
        logger.info(f"Reserva creada: {self.id} ({cliente.id} -> {servicio.id}, {horas} h)")

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA (si el servicio está disponible)."""
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar {self.id}: estado actual '{self._estado.value}'.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._servicio.id} no está disponible; no se confirma {self.id}.")
        self._estado = EstadoReserva.CONFIRMADA
        logger.info(f"Reserva {self.id} confirmada.")

    def cancelar(self, motivo="Sin motivo indicado"):
        """PENDIENTE o CONFIRMADA -> CANCELADA."""
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar {self.id}: estado actual '{self._estado.value}'.")
        self._estado = EstadoReserva.CANCELADA
        logger.info(f"Reserva {self.id} cancelada. Motivo: {motivo}")

    def procesar(self):
        """CONFIRMADA -> PROCESADA. Calcula el costo con try/except/else/finally."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"No se puede procesar {self.id}: estado actual '{self._estado.value}'.")
        try:
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self._servicio.id} dejó de estar disponible.")
            costo = self._servicio.costo_total(self._horas, self._impuesto,
                                               self._descuento, **self._opciones)
        except SoftwareFJError as e:
            self._estado = EstadoReserva.FALLIDA
            logger.error(f"Fallo al procesar {self.id}: {e}")
            raise ReservaInvalidaError(f"No se pudo procesar {self.id}: {e.mensaje}") from e
        except Exception as e:   # Error inesperado (p. ej. opción desconocida)
            self._estado = EstadoReserva.FALLIDA
            logger.error(f"Error inesperado al procesar {self.id}: {type(e).__name__}: {e}")
            raise CalculoInconsistenteError(f"Cálculo imposible para {self.id}: {e}") from e
        else:
            # Solo se ejecuta si NO hubo excepción
            self._costo = costo
            self._estado = EstadoReserva.PROCESADA
            logger.info(f"Reserva {self.id} procesada. Costo total: ${costo:,.2f}")
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            logger.debug(f"Fin del procesamiento de {self.id} (estado: {self._estado.value})")

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva {self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado.value} | {costo}")
