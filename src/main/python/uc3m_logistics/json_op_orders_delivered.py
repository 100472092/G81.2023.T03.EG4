from .json_op import Json_op
from .order_manager_config import JSON_FILES_PATH
from .order_management_exception import OrderManagementException
from .order_delivered import OrderDelivered
import json

class Json_op_order_delivered(Json_op):
    def __init__(self):
        self.path = JSON_FILES_PATH + "shipments_store.json"
        self.ip = "_OrderShipping__tracking_code"
        self.data_list = None

    def check_tracking_code(self, tracking_code):
        self.open()
        # search this tracking_code
        order = self.search(tracking_code)
        if order is None:
            raise OrderManagementException("tracking_code is not found")
        return order["_OrderShipping__delivery_day"]

    def open(self):
        try:
            with open(self.path, "r", encoding="utf-8", newline="") as file:
                self.data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            raise OrderManagementException("shipments_store not found")
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
    def save_shipments_delivered(self, tracking_code):
        super().open()
        myorder_del = OrderDelivered(tracking_code)
        self.data_list.append(myorder_del.__dict__)
        self.save()
