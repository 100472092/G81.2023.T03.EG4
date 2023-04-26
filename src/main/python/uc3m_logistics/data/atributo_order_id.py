"""atributo: OrderId"""

from .atributo import Atributos


# pylint: disable=too-few-public-methods
class OrderId(Atributos):
    """OrderId"""

    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._error_message = "order id is not valid"
        self._attr_value = self.validate_attr(valor)
