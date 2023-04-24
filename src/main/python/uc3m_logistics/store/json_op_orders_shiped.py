from .json_op import Json_op
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH

class Json_op_order_shiped(Json_op):
    def __init__(self):
        self.path = JSON_FILES_PATH + "shipments_store.json"
        self.ip = ""
        self.data_list = None

    def save_shipments_delivered(self, shipment):
        self.open()
        self.data_list.append(shipment.__dict__)
        self.save()