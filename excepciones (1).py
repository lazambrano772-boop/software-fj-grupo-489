"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el programa pueda capturar
cualquier error propio del dominio con un solo "except SoftwareFJError".
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema. Guarda un mensaje y un código de error."""

    codigo_defecto = "FJ-000"  # Código usado si la subclase no define otro

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)                     # Inicializa la excepción estándar
        self.mensaje = mensaje                        # Texto legible del error
        self.codigo = codigo or self.codigo_defecto   # Código para clasificar el error

    def __str__(self):
        # Formato uniforme: [CODIGO] mensaje
        return f"[{self.codigo}] {self.mensaje}"


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente inválidos o cliente inexistente/duplicado."""
    codigo_defecto = "FJ-100"


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros de un servicio inválidos o servicio inexistente."""
    codigo_defecto = "FJ-200"


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible para reservar."""
    codigo_defecto = "FJ-210"


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se pudo crear o procesar (suele encadenar otra causa)."""
    codigo_defecto = "FJ-300"


class OperacionNoPermitidaError(SoftwareFJError):
    """Transición de estado o acción no permitida sobre una reserva."""
    codigo_defecto = "FJ-310"


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio al ejecutar una operación."""
    codigo_defecto = "FJ-400"


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo de costos produjo valores inválidos o inconsistentes."""
    codigo_defecto = "FJ-500"
