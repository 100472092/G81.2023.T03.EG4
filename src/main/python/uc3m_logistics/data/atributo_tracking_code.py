"""atributo: trackingCode"""

from .Atributo import Atributos

class TrackingCode(Atributos):
    def __init__(self, value):
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "tracking_code format is not valid"
        self._attr_value = self.validate_attr(value)
