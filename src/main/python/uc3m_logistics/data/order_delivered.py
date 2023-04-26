"""orderDelivered"""

import os
from datetime import datetime
from .atributo_tracking_code import TrackingCode
from uc3m_logistics.store.json_op_orders_shiped import Json_op_order_shiped
from uc3m_logistics.exception.order_management_exception import OrderManagementException
class OrderDelivered():
    def __init__(self, tracking_code):
        self.tracking_code = TrackingCode(tracking_code).validate_attr(tracking_code)
        self.delivery_day = datetime.utcnow().__str__()
        self.check_date(self.check_tracking_code())

    def check_tracking_code(self):
        store = Json_op_order_shiped()
        store.open()
        # search this tracking_code
        order = store.search(self.tracking_code)

        if order is None:
            if os.path.isfile(store.path):
                raise OrderManagementException("tracking_code is not found")
            raise OrderManagementException("shipments_store not found")
        return order["_OrderShipping__delivery_day"]
    def check_date(self, del_timestamp):
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
