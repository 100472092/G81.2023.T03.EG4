"""atributo: trackingCode"""

from .atributo import Atributos


# pylint: disable=too-few-public-methods
class TrackingCode(Atributos):
    """TrackingCode"""

    def __init__(self, value):
        super().__init__()
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "tracking_code format is not valid"
        self._attr_value = self.validate_attr(value)
