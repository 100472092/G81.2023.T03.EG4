"""json module for shipments_store"""
# pylint: disable=import-error
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from .json_op import JsonOp


class JsonOpOrderShiped():
    """json module for shipments_store"""

    # pylint: disable=invalid-name
    class __JsonOpOrderShiped(JsonOp):
        def __init__(self):
            super().__init__()
            self.path = JSON_FILES_PATH + "shipments_store.json"
            self.key = "_OrderShipping__tracking_code"
            self.data_list = None

        def save_shipments_delivered(self, shipment):
            """saves new shipment"""
            self.open()
            self.data_list.append(shipment.__dict__)
            self.save()

    instance = None

    def __new__(cls):
        if not JsonOpOrderShiped.instance:
            JsonOpOrderShiped.instance = JsonOpOrderShiped.__JsonOpOrderShiped()
        return JsonOpOrderShiped.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)
