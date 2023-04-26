"""atributo: orderType"""

from .atributo import Atributos

class OrderType(Atributos):
    """OrderType"""
    def __init__(self, valor):
        self._validation_pattern = r"Regular|Premium"
        self._error_message = "order_type is not valid"
        self._attr_value = self.validate_attr(valor)
