"""json module for orders_store"""

# pylint: disable=import-error
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from .json_op import JsonOp


class JsonOpOrderStore():
    """json module for orders_store"""

    # pylint: disable=invalid-name
    class __JsonOpOrderStore(JsonOp):
        def __init__(self):
            super().__init__()
            self.path = JSON_FILES_PATH + "orders_store.json"
            self.key = "_OrderRequest__order_id"
            self.data_list = None

        def save_order_id(self, data):
            """saves a new order"""
            self.open()
            if self.search(data.order_id) is not None:
                raise OrderManagementException("order_id is already registered in orders_store")
            self.data_list.append(data.__dict__)
            self.save()

    instance = None

    def __new__(cls):
        if not JsonOpOrderStore.instance:
            JsonOpOrderStore.instance = JsonOpOrderStore.__JsonOpOrderStore()
        return JsonOpOrderStore.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)
