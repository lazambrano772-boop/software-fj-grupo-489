"""
gestor.py
GestorSoftwareFJ: administra clientes, servicios y reservas en listas internas
(sin base de datos).
"""
from entidades import Cliente
from excepciones import (ClienteInvalidoError, ParametroFaltanteError,
                         ReservaInvalidaError, ServicioInvalidoError)
from logger_config import obtener_logger
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

logger = obtener_logger()


class GestorSoftwareFJ:
    TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo,
                      "asesoria": AsesoriaEspecializada}

    def __init__(self):
        self._clientes = []    # Lista interna de clientes
        self._servicios = []   # Lista interna de servicios
        self._reservas = []    # Lista interna de reservas

    # ----------------- clientes -----------------
    def registrar_cliente(self, **datos):
        doc = str(datos.get("documento", "")).strip()
        if any(c.documento == doc for c in self._clientes):
            raise ClienteInvalidoError(f"Ya existe un cliente con el documento {doc}.")
        try:
            cliente = Cliente(**datos)
        except TypeError as e:   # Falta o sobra algún parámetro
            raise ParametroFaltanteError(f"Parámetros incorrectos al registrar cliente: {e}") from e
        else:
            self._clientes.append(cliente)
            return cliente

    def buscar_cliente(self, id_cliente):
        for c in self._clientes:
            if c.id == id_cliente:
                return c
        raise ClienteInvalidoError(f"No existe el cliente '{id_cliente}'.")

    # ----------------- servicios -----------------
    def crear_servicio(self, tipo, **datos):
        clase = self.TIPOS_SERVICIO.get(tipo)
        if clase is None:
            raise ServicioInvalidoError(
                f"Tipo de servicio '{tipo}' no existe. Opciones: {', '.join(self.TIPOS_SERVICIO)}.")
        try:
            servicio = clase(**datos)
        except TypeError as e:
            raise ParametroFaltanteError(f"Parámetros incorrectos al crear servicio '{tipo}': {e}") from e
        else:
            self._servicios.append(servicio)
            return servicio

    def buscar_servicio(self, id_servicio):
        for s in self._servicios:
            if s.id == id_servicio:
                return s
        raise ServicioInvalidoError(f"No existe el servicio '{id_servicio}'.")

    # ----------------- reservas -----------------
    def crear_reserva(self, id_cliente, id_servicio, horas, impuesto=None, descuento=None, **opciones):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        reserva = Reserva(cliente, servicio, horas, impuesto, descuento, **opciones)
        self._reservas.append(reserva)
        return reserva

    def buscar_reserva(self, id_reserva):
        for r in self._reservas:
            if r.id == id_reserva:
                return r
        raise ReservaInvalidaError(f"No existe la reserva '{id_reserva}'.")

    def confirmar_reserva(self, id_reserva):
        self.buscar_reserva(id_reserva).confirmar()

    def cancelar_reserva(self, id_reserva, motivo="Sin motivo indicado"):
        self.buscar_reserva(id_reserva).cancelar(motivo)

    def procesar_reserva(self, id_reserva):
        return self.buscar_reserva(id_reserva).procesar()

    # ----------------- resumen -----------------
    def resumen(self):
        return {"clientes": len(self._clientes), "servicios": len(self._servicios),
                "reservas": len(self._reservas)}

    def listar_reservas(self):
        return [str(r) for r in self._reservas]
