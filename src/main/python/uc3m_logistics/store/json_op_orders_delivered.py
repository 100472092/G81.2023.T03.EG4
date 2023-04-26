from .json_op import Json_op
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
import json

class Json_op_order_delivered():
    class __Json_op_order_delivered(Json_op):
        def __init__(self):
            self.path = JSON_FILES_PATH + "shipments_delivered.json"
            self.ip = "_OrderShipping__tracking_code"
            self.data_list = None
        def open(self):
            try:
                with open(self.path, "r", encoding="utf-8", newline="") as file:
                    self.data_list = json.load(file)
            except FileNotFoundError:
                # file is not found , so  init my data_list
                raise OrderManagementException("shipments_store not found")
            except json.JSONDecodeError as ex:
                raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        def save_shipments_delivered(self, order_del):
            super().open()

            self.data_list.append(order_del.__dict__)
            print(self.data_list)
            self.save()
    instance = None

    def __new__(self):
        if not Json_op_order_delivered.instance:
            Json_op_order_delivered.instance = Json_op_order_delivered.__Json_op_order_delivered()
        return Json_op_order_delivered.instance

    def __getattr__(self, item):
        return  getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)
