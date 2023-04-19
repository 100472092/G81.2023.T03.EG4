from .json_op import Json_op
from .order_manager_config import JSON_FILES_PATH
from .order_management_exception import OrderManagementException


class Json_op_order_store(Json_op):
    def __init__(self):
        self.path = JSON_FILES_PATH + "orders_store.json"
        self.ip = ""
        self.data_list = None

    def save_order_id(self, data):
        self.open()
        if self.search("_OrderRequest__order_id", data.order_id):
            raise OrderManagementException("order_id is already registered in orders_store")
        self.data_list.append(data.__dict__)
        self.save()
