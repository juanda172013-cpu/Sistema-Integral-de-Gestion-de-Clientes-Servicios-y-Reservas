"""Configuración del archivo de logs (eventos y errores)."""
import logging  # Módulo estándar de registro de eventos
import os  # Para manejar rutas y carpetas

# Carpeta logs junto a este archivo
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def obtener_logger():
    """Devuelve el logger único del sistema, escribiendo en logs/eventos.log."""
    os.makedirs(RUTA_LOGS, exist_ok=True)  # Crea la carpeta si no existe
    log = logging.getLogger("software_fj")  # Obtiene el logger por nombre
    if not log.handlers:  # Evita duplicar manejadores si se llama varias veces
        log.setLevel(logging.DEBUG)  # Registra desde nivel DEBUG
        manejador = logging.FileHandler(os.path.join(RUTA_LOGS, "eventos.log"), encoding="utf-8")  # Archivo de salida
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # Fecha | nivel | mensaje
        manejador.setFormatter(formato)  # Asigna el formato al manejador
        log.addHandler(manejador)  # Añade el manejador al logger
    return log  # Devuelve el logger configurado
