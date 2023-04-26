"""atributo: productId"""
# pylint: disable=import-error
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from .atributo import Atributos


# pylint: disable=too-few-public-methods

class ProductId(Atributos):
    """product_id"""

    def __init__(self, valor):
        super().__init__()
        self._validation_pattern = r"^[0-9]{13}$"
        self._error_message = "Invalid EAN13 code string"
        self._attr_value = self.validate_attr(valor)

    def validate_attr(self, valor):
        """method vor validating a ean13 code"""
        checksum = 0
        code_read = -1
        super().validate_attr(valor)

        for i, digit in enumerate(reversed(valor)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            return valor

        raise OrderManagementException("Invalid EAN13 control digit")
