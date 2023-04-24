from .Atributo import Atributos

class Phone_number(Atributos):
    def __init__(self, valor):
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self.validate_attr(valor)