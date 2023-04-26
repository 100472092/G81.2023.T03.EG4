"""atributo:email"""

from .Atributo import Atributos

class Email(Atributos):
    def __init__(self, valor):
        self._validation_pattern = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self._error_message = "contact email is not valid"
        self._attr_value = self.validate_attr(valor)
