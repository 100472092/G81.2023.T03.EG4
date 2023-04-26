"""atributo: phoneNumber"""
from .atributo import Atributos

# pylint: disable=too-few-public-methods
class PhoneNumber(Atributos):
    """Phone Number"""
    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self.validate_attr(valor)
