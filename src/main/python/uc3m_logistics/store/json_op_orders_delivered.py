"""Json operations for order_delivered_store"""
# pylint: disable=import-error
import json
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from .json_op import JsonOp


class JsonOpOrderDelivered():
    """Json operations for order_delivered_store"""

    # pylint: disable=invalid-name
    class __JsonOpOrderDelivered(JsonOp):
        def __init__(self):
            super().__init__()
            self.path = JSON_FILES_PATH + "shipments_delivered.json"
            self.key = "_OrderShipping__tracking_code"
            self.data_list = None

        def open(self):
            """rewrites open"""
            try:
                with open(self.path, "r", encoding="utf-8", newline="") as file:
                    self.data_list = json.load(file)
            except FileNotFoundError as exc:
                # file is not found , so  init my data_list
                raise OrderManagementException("shipments_store not found") from exc
            except json.JSONDecodeError as ex:
                raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        def save_shipments_delivered(self, order_del):
            """save to the store"""
            super().open()

            self.data_list.append(order_del.__dict__)
            print(self.data_list)
            self.save()

    instance = None

    def __new__(cls):
        if not JsonOpOrderDelivered.instance:
            JsonOpOrderDelivered.instance = JsonOpOrderDelivered.__JsonOpOrderDelivered()
        return JsonOpOrderDelivered.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)
