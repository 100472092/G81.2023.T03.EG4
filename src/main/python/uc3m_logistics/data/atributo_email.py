"""atributo:email"""

from .atributo import Atributos


# pylint: disable=too-few-public-methods
class Email(Atributos):
    """Email"""

    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self._error_message = "contact email is not valid"
        self._attr_value = self.validate_attr(valor)
