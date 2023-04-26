"""atributo: orderType"""
# pylint:disable=import-error
from .atributo import Atributos


# pylint: disable=too-few-public-methods

class OrderType(Atributos):
    """OrderType"""

    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r"Regular|Premium"
        self._error_message = "order_type is not valid"
        self._attr_value = self.validate_attr(valor)
