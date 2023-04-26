"""atributo: zipCode"""
# pylint: disable=import-error
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from .atributo import Atributos


# pylint: disable=too-few-public-methods
class ZipCode(Atributos):
    """ZipCode"""

    def __init__(self, valor):
        super().__init__()
        self._attr_value = self.validate_attr(valor)

    def validate_attr(self, valor):
        """validates for zip_code"""
        if valor.isnumeric() and len(valor) == 5:
            if int(valor) > 52999 or int(valor) < 1000:
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return valor
