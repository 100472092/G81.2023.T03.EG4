"""Atributo clase abstracta"""

import re
from uc3m_logistics.exception.order_management_exception import OrderManagementException

class Atributos:
    def __init__(self):
        self._validation_pattern = ""
        self._error_message = ""
        self._attr_value = ""

    def validate_attr(self, valor):
        """validates the attr value"""
        myregex = re.compile(self._validation_pattern)
        regex_match = myregex.fullmatch(valor)
        if not regex_match:
            raise OrderManagementException(self._error_message)
        return valor
