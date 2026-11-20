"""
logger_config.py
Configuración del archivo de logs (logs/software_fj.log).

Todos los módulos obtienen el mismo logger llamando a obtener_logger(),
así todos los errores y eventos quedan en un único archivo.
"""
# Importa las herramientas necesarias para registrar eventos y gestionar archivos.
import logging
import os

# Carpeta y archivo donde se guardan los registros
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")

# Configura y devuelve el logger utilizado por los módulos del sistema.
def obtener_logger(nombre="software_fj"):
    """Devuelve el logger del sistema, configurándolo solo la primera vez."""
    # Obtiene el logger asociado al nombre indicado.
    logger = logging.getLogger(nombre)
    if logger.handlers:            # Si ya fue configurado, se reutiliza
        return logger

    os.makedirs(RUTA_LOGS, exist_ok=True)   # Crea la carpeta logs/ si no existe
    logger.setLevel(logging.DEBUG)          # Registra todos los niveles
    logger.propagate = False                # Evita mensajes duplicados en consola
    # Define el formato y la fecha de los mensajes registrados.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    # Archivo en UTF-8 para conservar tildes y la letra ñ
    manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger
