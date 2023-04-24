from .Atributo import Atributos
from uc3m_logistics.exception.order_management_exception import OrderManagementException

class Zip_code(Atributos):
    def __init__(self, valor):
        self._attr_value = self.validate_attr(valor)

    def validate_attr(self, zip_code):
        if zip_code.isnumeric() and len(zip_code) == 5:
            if (int(zip_code) > 52999 or int(zip_code) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return zip_code