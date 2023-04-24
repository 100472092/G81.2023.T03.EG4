from .json_op import Json_op
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException


class Json_op_order_store(Json_op):
    def __init__(self):
        self.path = JSON_FILES_PATH + "orders_store.json"
        self.ip = "_OrderRequest__order_id"
        self.data_list = None

    def save_order_id(self, data):
        self.open()
        if self.search(data.order_id) is not None:
            raise OrderManagementException("order_id is already registered in orders_store")
        self.data_list.append(data.__dict__)
        self.save()
