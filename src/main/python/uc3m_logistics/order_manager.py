"""Module """

# pylint: disable=import-error
from uc3m_logistics.data.order_request import OrderRequest
from uc3m_logistics.data.order_shipping import OrderShipping
from uc3m_logistics.store.json_op_orders_store import JsonOpOrderStore
from uc3m_logistics.store.json_op_orders_shiped import JsonOpOrderShiped
from uc3m_logistics.store.json_op_orders_delivered import JsonOpOrderDelivered
from uc3m_logistics.data.order_delivered import OrderDelivered

# pylint: disable=too-few-public-methods
class OrderManager:
    """Class for providing the methods for managing the orders process"""

    # pylint: disable=invalid-name
    class __OrderManager:
        def __init__(self):
            pass

        # pylint: disable=too-many-arguments
        def register_order(self, product_id,
                           order_type,
                           address,
                           phone_number,
                           zip_code):
            """Register the orders into the order's file"""
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)
            store = JsonOpOrderStore()
            store.save_order_id(my_order)
            return my_order.order_id

        def send_product(self, input_file):
            """Sends the order included in the input_file"""
            # data = self.read_json_file(input_file)
            my_sign = OrderShipping(input_file)

            # save the OrderShipping in shipments_store.json
            store = JsonOpOrderShiped()
            store.save_shipments_delivered(my_sign)
            return my_sign.tracking_code

        def deliver_product(self, tracking_code):
            """Register the delivery of the product"""
            order_deliv = OrderDelivered(tracking_code)
            store = JsonOpOrderDelivered()
            store.save_shipments_delivered(order_deliv)
            return True

    instance = None

    def __new__(cls):
        if not OrderManager.instance:
            OrderManager.instance = OrderManager.__OrderManager()
        return OrderManager.instance
