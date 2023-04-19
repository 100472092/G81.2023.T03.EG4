from .Atributo import Atributos

class Address(Atributos):
    def __init__(self, valor):
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._error_message = "address is not valid"
        self._attr_value = self.validate_attr(valor)