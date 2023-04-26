"""atributo: OrderId"""

from .Atributo import Atributos

class OrderId(Atributos):
    def __init__(self, valor):
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._error_message = "order id is not valid"
        self._attr_value = self.validate_attr(valor)
