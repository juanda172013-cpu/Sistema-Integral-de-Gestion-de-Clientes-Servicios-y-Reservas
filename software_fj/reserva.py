"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente  # Para verificar el tipo de cliente
from excepciones import (CalculoInconsistenteError, ErrorSoftwareFJ, OperacionNoPermitidaError,
                         ParametroInvalidoError, ReservaInvalidaError, ServicioNoDisponibleError)  # Excepciones propias
from logger import obtener_logger  # Logger del sistema
from servicios import Servicio  # Para verificar el tipo de servicio

log = obtener_logger()  # Logger compartido


class Reserva:
    """Reserva con estados: pendiente, confirmada, procesada o cancelada."""

    def __init__(self, identificador, cliente, servicio, duracion):  # Constructor
        if not isinstance(cliente, Cliente):  # El cliente debe ser un Cliente real
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")  # Error de cliente
        if not isinstance(servicio, Servicio):  # El servicio debe ser un Servicio real
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")  # Error de servicio
        try:  # Intenta validar la duración con las reglas del servicio
            servicio.validar_parametros(duracion)  # Validación polimórfica
        except ParametroInvalidoError as error:  # Si la duración es inválida
            raise ReservaInvalidaError("Duración no válida para el servicio.") from error  # Encadena la causa original
        self.id = identificador  # Identificador de la reserva
        self.cliente = cliente  # Cliente que reserva
        self.servicio = servicio  # Servicio reservado
        self.duracion = duracion  # Duración (horas o días)
        self.estado = "pendiente"  # Estado inicial
        self.costo = None  # Se calcula al procesar

    def confirmar(self):  # Confirma la reserva
        if self.estado != "pendiente":  # Solo se confirma desde pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")  # Error de estado
        if not self.servicio.disponible:  # El servicio debe estar disponible
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")  # Error
        self.estado = "confirmada"  # Cambia el estado
        log.info(f"Reserva {self.id} confirmada.")  # Registra el evento

    def cancelar(self):  # Cancela la reserva
        if self.estado in ("cancelada", "procesada"):  # No se cancela si ya terminó o se canceló
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self.estado}.")  # Error de estado
        self.estado = "cancelada"  # Cambia el estado
        log.info(f"Reserva {self.id} cancelada.")  # Registra el evento

    def procesar(self, impuesto=None, descuento=0.0):  # Procesa la reserva (calcula costo)
        if self.estado != "confirmada":  # Debe estar confirmada
            raise OperacionNoPermitidaError(f"Solo se procesan reservas confirmadas (estado: {self.estado}).")  # Error
        try:  # Bloque try/except/else/finally
            costo = self.servicio.calcular_costo(self.duracion, impuesto, descuento)  # Calcula el costo
        except ErrorSoftwareFJ as error:  # Si el cálculo falla
            raise CalculoInconsistenteError(f"No se pudo procesar la reserva {self.id}.") from error  # Encadena
        else:  # Solo si no hubo excepción
            self.costo = costo  # Guarda el costo
            self.estado = "procesada"  # Cambia el estado
            log.info(f"Reserva {self.id} procesada. Costo total: ${costo:,.2f}")  # Registra el éxito
            return costo  # Devuelve el costo
        finally:  # Siempre se ejecuta
            log.debug(f"Fin del intento de procesamiento de la reserva {self.id}.")  # Registro de cierre

    def describir(self):  # Descripción de la reserva
        return (f"Reserva #{self.id} | {self.cliente.nombre} | {self.servicio.nombre} | "
                f"duración {self.duracion} | estado {self.estado}")  # Texto descriptivo
