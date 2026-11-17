"""Gestor del sistema: listas internas y operaciones protegidas contra errores."""
from entidades import Cliente  # Clase Cliente
from excepciones import ErrorSoftwareFJ, ParametroInvalidoError  # Excepciones propias
from logger import obtener_logger  # Logger del sistema
from reserva import Reserva  # Clase Reserva

log = obtener_logger()  # Logger compartido


class GestorFJ:
    """Administra clientes, servicios y reservas en listas (sin base de datos)."""

    def __init__(self):  # Constructor
        self.clientes = []  # Lista interna de clientes
        self.servicios = []  # Lista interna de servicios
        self.reservas = []  # Lista interna de reservas

    @staticmethod
    def _exigir(datos, *campos):  # Verifica parámetros faltantes
        for campo in campos:  # Recorre cada campo requerido
            try:  # Intenta leerlo
                datos[campo]  # Acceso que puede fallar
            except KeyError as error:  # Si falta
                raise ParametroInvalidoError(f"Falta el parámetro obligatorio '{campo}'.") from error  # Encadena KeyError

    def registrar_cliente(self, **datos):  # Registra un cliente de forma segura
        try:  # Intenta crear el cliente
            self._exigir(datos, "nombre", "correo", "telefono")  # Valida campos requeridos
            cliente = Cliente(len(self.clientes) + 1, datos["nombre"], datos["correo"], datos["telefono"])  # Crea
        except ErrorSoftwareFJ as error:  # Error controlado del sistema
            log.error(f"Registro de cliente fallido: {error}")  # Registra el error
            return None  # El sistema sigue funcionando
        except Exception as error:  # Error inesperado
            log.critical(f"Error inesperado registrando cliente: {error!r}")  # Registra el error grave
            return None  # El sistema sigue funcionando
        else:  # Si todo salió bien
            self.clientes.append(cliente)  # Añade a la lista
            log.info(f"Cliente registrado: {cliente.describir()}")  # Registra el evento
            return cliente  # Devuelve el cliente
        finally:  # Siempre se ejecuta
            log.debug("Fin de registrar_cliente.")  # Registro de cierre

    def crear_servicio(self, clase, **datos):  # Crea un servicio de cualquier tipo
        try:  # Intenta crearlo
            servicio = clase(len(self.servicios) + 1, **datos)  # Instancia la clase indicada
        except ErrorSoftwareFJ as error:  # Error controlado
            log.error(f"Creación de servicio fallida: {error}")  # Registra el error
            return None  # Continúa
        except TypeError as error:  # Parámetros faltantes o sobrantes / clase abstracta
            log.error(f"Parámetros incorrectos al crear servicio: {error}")  # Registra el error
            return None  # Continúa
        else:  # Si salió bien
            self.servicios.append(servicio)  # Añade a la lista
            log.info(f"Servicio creado: {servicio.describir()}")  # Registra el evento
            return servicio  # Devuelve el servicio

    def crear_reserva(self, cliente, servicio, duracion):  # Crea y confirma una reserva
        try:  # Intenta crear y confirmar
            reserva = Reserva(len(self.reservas) + 1, cliente, servicio, duracion)  # Crea la reserva
            reserva.confirmar()  # Confirma (puede fallar si no hay disponibilidad)
        except ErrorSoftwareFJ as error:  # Error controlado
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""  # Muestra la excepción encadenada
            log.error(f"Reserva fallida: {error}{causa}")  # Registra el error
            return None  # Continúa
        else:  # Si salió bien
            self.reservas.append(reserva)  # Añade a la lista
            return reserva  # Devuelve la reserva

    def procesar_reserva(self, reserva, impuesto=None, descuento=0.0):  # Procesa una reserva de forma segura
        try:  # Intenta procesar
            return reserva.procesar(impuesto, descuento)  # Devuelve el costo
        except ErrorSoftwareFJ as error:  # Error controlado
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""  # Excepción encadenada
            log.error(f"Procesamiento fallido: {error}{causa}")  # Registra el error
        except AttributeError as error:  # Reserva None u objeto incorrecto
            log.error(f"Reserva inexistente: {error}")  # Registra el error
        return None  # Continúa sin caerse

    def cancelar_reserva(self, reserva):  # Cancela una reserva de forma segura
        try:  # Intenta cancelar
            reserva.cancelar()  # Cancela
            return True  # Éxito
        except ErrorSoftwareFJ as error:  # Error controlado
            log.error(f"Cancelación fallida: {error}")  # Registra el error
        except AttributeError as error:  # Reserva None
            log.error(f"Reserva inexistente: {error}")  # Registra el error
        return False  # Falló pero el sistema sigue
