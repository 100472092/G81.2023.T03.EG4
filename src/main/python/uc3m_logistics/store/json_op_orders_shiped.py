from .json_op import Json_op
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH

class Json_op_order_shiped():

    class __Json_op_order_shiped(Json_op):
        def __init__(self):
            self.path = JSON_FILES_PATH + "shipments_store.json"
            self.ip = "_OrderShipping__tracking_code"
            self.data_list = None

        def save_shipments_delivered(self, shipment):
            self.open()
            self.data_list.append(shipment.__dict__)
            self.save()

    instance = None

    def __new__(self):
        if not Json_op_order_shiped.instance:
            Json_op_order_shiped.instance = Json_op_order_shiped.__Json_op_order_shiped()
        return Json_op_order_shiped.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)