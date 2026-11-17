"""Clase abstracta EntidadBase y clase Cliente."""
import re  # Expresiones regulares para validar correo y teléfono
from abc import ABC, abstractmethod  # Herramientas para clases abstractas

from excepciones import ClienteInvalidoError, ParametroInvalidoError  # Excepciones propias


class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    def __init__(self, identificador, nombre):  # Constructor común
        if not isinstance(nombre, str) or not nombre.strip():  # Nombre debe ser texto no vacío
            raise ParametroInvalidoError("El nombre es obligatorio y debe ser texto.")  # Error si no cumple
        self._id = identificador  # Atributo protegido: identificador
        self._nombre = nombre.strip()  # Atributo protegido: nombre sin espacios sobrantes

    @property  # Lectura controlada del id (encapsulación)
    def id(self):
        return self._id  # Devuelve el identificador

    @property  # Lectura controlada del nombre
    def nombre(self):
        return self._nombre  # Devuelve el nombre

    @abstractmethod  # Obliga a las hijas a implementarlo
    def describir(self):
        """Devuelve una descripción en texto de la entidad."""

    def __str__(self):  # Representación por defecto
        return self.describir()  # Usa el método polimórfico describir


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")  # Formato básico de correo
    PATRON_TELEFONO = re.compile(r"^\d{7,10}$")  # Teléfono de 7 a 10 dígitos

    def __init__(self, identificador, nombre, correo, telefono):  # Constructor
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:  # Valida nombre mínimo
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")  # Error de nombre
        super().__init__(identificador, nombre)  # Inicializa la parte base
        self.__correo = None  # Atributo privado (name mangling): correo
        self.__telefono = None  # Atributo privado: teléfono
        self.correo = correo  # Usa el setter con validación
        self.telefono = telefono  # Usa el setter con validación

    @property  # Getter del correo
    def correo(self):
        return self.__correo  # Devuelve el correo privado

    @correo.setter  # Setter con validación del correo
    def correo(self, valor):
        if not isinstance(valor, str) or not self.PATRON_CORREO.match(valor):  # Comprueba formato
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")  # Error si no cumple
        self.__correo = valor  # Guarda el correo válido

    @property  # Getter del teléfono
    def telefono(self):
        return self.__telefono  # Devuelve el teléfono privado

    @telefono.setter  # Setter con validación del teléfono
    def telefono(self, valor):
        if not isinstance(valor, str) or not self.PATRON_TELEFONO.match(valor):  # Comprueba formato
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r}")  # Error si no cumple
        self.__telefono = valor  # Guarda el teléfono válido

    def describir(self):  # Implementación del método abstracto
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | {self.telefono}"  # Texto descriptivo
