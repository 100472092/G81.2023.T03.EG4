"""atributo: address"""

from .atributo import Atributos


# pylint: disable=too-few-public-methods
class Address(Atributos):
    """Address"""

    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._error_message = "address is not valid"
        self._attr_value = self.validate_attr(valor)
