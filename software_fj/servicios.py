"""Clase abstracta Servicio y tres servicios especializados."""
from abc import ABC, abstractmethod  # Clases abstractas

from entidades import EntidadBase  # Clase base general
from excepciones import CalculoInconsistenteError, ParametroInvalidoError  # Excepciones propias


def _es_numero(valor):
    """Indica si el valor es numérico (int/float) y no booleano."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)  # Excluye bool


class Servicio(EntidadBase, ABC):
    """Clase abstracta de la que heredan todos los servicios."""

    IMPUESTO_DEFECTO = 0.19  # IVA por defecto (19 %)

    def __init__(self, identificador, nombre, tarifa, disponible=True):  # Constructor
        super().__init__(identificador, nombre)  # Inicializa la parte base
        if not _es_numero(tarifa) or tarifa <= 0:  # La tarifa debe ser número positivo
            raise ParametroInvalidoError(f"Tarifa inválida: {tarifa!r}")  # Error de tarifa
        self._tarifa = float(tarifa)  # Tarifa protegida
        self._disponible = bool(disponible)  # Estado de disponibilidad

    @property  # Getter de la tarifa
    def tarifa(self):
        return self._tarifa  # Devuelve la tarifa

    @property  # Getter de disponibilidad
    def disponible(self):
        return self._disponible  # Devuelve si está disponible

    @disponible.setter  # Setter de disponibilidad
    def disponible(self, valor):
        self._disponible = bool(valor)  # Convierte a booleano y guarda

    @abstractmethod  # Cada servicio calcula su costo distinto
    def calcular_costo(self, duracion, impuesto=None, descuento=0.0):
        """Sobrecarga por parámetros opcionales: (duracion), (duracion, impuesto) o (duracion, impuesto, descuento)."""

    @abstractmethod  # Cada servicio valida a su manera
    def validar_parametros(self, duracion):
        """Lanza ParametroInvalidoError si la duración no es válida."""

    def _aplicar_impuesto_descuento(self, base, impuesto, descuento):
        """Aplica descuento e impuesto al costo base con validaciones."""
        if impuesto is None:  # Si no se envió impuesto
            impuesto = self.IMPUESTO_DEFECTO  # Usa el impuesto por defecto
        if not _es_numero(impuesto) or impuesto < 0:  # Valida impuesto
            raise CalculoInconsistenteError(f"Impuesto inválido: {impuesto!r}")  # Error de impuesto
        if not _es_numero(descuento) or not 0 <= descuento < 1:  # Descuento entre 0 y 1 (sin incluir 1)
            raise CalculoInconsistenteError(f"Descuento inválido: {descuento!r}")  # Error de descuento
        total = base * (1 - descuento) * (1 + impuesto)  # Fórmula del costo final
        if total <= 0:  # Un costo no positivo es inconsistente
            raise CalculoInconsistenteError("El costo calculado no es positivo.")  # Error de cálculo
        return round(total, 2)  # Devuelve el total redondeado


class ReservaSala(Servicio):
    """Reserva de salas, cobrada por hora."""

    def __init__(self, identificador, nombre, tarifa, capacidad, disponible=True):  # Constructor
        super().__init__(identificador, nombre, tarifa, disponible)  # Inicializa la clase padre
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:  # Capacidad entera > 0
            raise ParametroInvalidoError(f"Capacidad inválida: {capacidad!r}")  # Error de capacidad
        self._capacidad = capacidad  # Personas que caben en la sala

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not _es_numero(duracion) or not 1 <= duracion <= 12:  # De 1 a 12 horas
            raise ParametroInvalidoError(f"Horas de sala inválidas (1-12): {duracion!r}")  # Error de duración

    def calcular_costo(self, duracion, impuesto=None, descuento=0.0):  # Sobrescribe el cálculo
        self.validar_parametros(duracion)  # Valida antes de calcular
        base = self._tarifa * duracion  # Costo = tarifa por hora * horas
        return self._aplicar_impuesto_descuento(base, impuesto, descuento)  # Aplica impuesto y descuento

    def describir(self):  # Sobrescribe la descripción
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}) - ${self._tarifa:,.0f}/hora"  # Texto descriptivo


class AlquilerEquipo(Servicio):
    """Alquiler de equipos, cobrado por día."""

    def __init__(self, identificador, nombre, tarifa, cantidad=1, disponible=True):  # Constructor
        super().__init__(identificador, nombre, tarifa, disponible)  # Inicializa la clase padre
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:  # Cantidad entera > 0
            raise ParametroInvalidoError(f"Cantidad inválida: {cantidad!r}")  # Error de cantidad
        self._cantidad = cantidad  # Unidades alquiladas

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not 1 <= duracion <= 30:  # Días enteros 1-30
            raise ParametroInvalidoError(f"Días de alquiler inválidos (1-30): {duracion!r}")  # Error de duración

    def calcular_costo(self, duracion, impuesto=None, descuento=0.0):  # Sobrescribe el cálculo
        self.validar_parametros(duracion)  # Valida antes de calcular
        base = self._tarifa * duracion * self._cantidad  # Tarifa diaria * días * unidades
        if duracion > 7:  # Alquiler largo
            descuento = max(descuento, 0.05)  # Garantiza al menos 5 % de descuento
        return self._aplicar_impuesto_descuento(base, impuesto, descuento)  # Aplica impuesto y descuento

    def describir(self):  # Sobrescribe la descripción
        return f"Equipo '{self.nombre}' x{self._cantidad} - ${self._tarifa:,.0f}/día"  # Texto descriptivo


class AsesoriaEspecializada(Servicio):
    """Asesoría por horas con recargo según el nivel del asesor."""

    NIVELES = {"junior": 1.0, "senior": 1.5}  # Multiplicador por nivel

    def __init__(self, identificador, nombre, tarifa, nivel="junior", disponible=True):  # Constructor
        super().__init__(identificador, nombre, tarifa, disponible)  # Inicializa la clase padre
        if nivel not in self.NIVELES:  # El nivel debe existir
            raise ParametroInvalidoError(f"Nivel inválido: {nivel!r}")  # Error de nivel
        self._nivel = nivel  # Nivel del asesor

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not _es_numero(duracion) or not 1 <= duracion <= 8:  # De 1 a 8 horas
            raise ParametroInvalidoError(f"Horas de asesoría inválidas (1-8): {duracion!r}")  # Error de duración

    def calcular_costo(self, duracion, impuesto=None, descuento=0.0):  # Sobrescribe el cálculo
        self.validar_parametros(duracion)  # Valida antes de calcular
        base = self._tarifa * duracion * self.NIVELES[self._nivel]  # Tarifa * horas * multiplicador
        return self._aplicar_impuesto_descuento(base, impuesto, descuento)  # Aplica impuesto y descuento

    def describir(self):  # Sobrescribe la descripción
        return f"Asesoría '{self.nombre}' nivel {self._nivel} - ${self._tarifa:,.0f}/hora"  # Texto descriptivo
