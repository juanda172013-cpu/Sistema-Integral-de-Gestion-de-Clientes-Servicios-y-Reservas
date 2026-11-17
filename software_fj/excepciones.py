"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las demás heredan de ella."""

    def __init__(self, mensaje, codigo="FJ-000"):  # Constructor con mensaje y código de error
        super().__init__(mensaje)  # Llama al constructor de Exception con el mensaje
        self.codigo = codigo  # Guarda el código para identificar el tipo de error

    def __str__(self):  # Representación en texto de la excepción
        return f"[{self.codigo}] {super().__str__()}"  # Devuelve código + mensaje


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente inválidos (nombre, correo, teléfono)."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-101")  # Código propio de cliente


class ParametroInvalidoError(ErrorSoftwareFJ):
    """Parámetro inválido o faltante."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-102")  # Código propio de parámetros


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no está disponible."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-103")  # Código propio de disponibilidad


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Intento de reserva incorrecto."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-104")  # Código propio de reservas


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Operación no permitida según el estado actual."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-105")  # Código propio de operaciones


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Cálculo de costos inconsistente."""

    def __init__(self, mensaje):  # Constructor
        super().__init__(mensaje, "FJ-106")  # Código propio de cálculos
