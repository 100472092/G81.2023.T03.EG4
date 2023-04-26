"""Module """
from uc3m_logistics.data.order_request import OrderRequest
from uc3m_logistics.data.order_shipping import OrderShipping
from uc3m_logistics.store.json_op_orders_store import Json_op_order_store
from uc3m_logistics.store.json_op_orders_shiped import Json_op_order_shiped
from uc3m_logistics.store.json_op_orders_delivered import Json_op_order_delivered
from uc3m_logistics.data.order_delivered import OrderDelivered
class OrderManager:
    """Class for providing the methods for managing the orders process"""
    class __OrderManager:
        def __init__(self):
            pass

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
            store = Json_op_order_store()
            store.save_order_id(my_order)
            return my_order.order_id

        # pylint: disable=too-many-locals
        def send_product(self, input_file):
            """Sends the order included in the input_file"""
            # data = self.read_json_file(input_file)
            my_sign = OrderShipping(input_file)

            # save the OrderShipping in shipments_store.json
            store = Json_op_order_shiped()
            store.save_shipments_delivered(my_sign)
            return my_sign.tracking_code

        def deliver_product(self, tracking_code):
            """Register the delivery of the product"""
            order_deliv = OrderDelivered(tracking_code)
            store = Json_op_order_delivered()
            store.save_shipments_delivered(order_deliv)
            return True

    instance = None
    def __new__(cls):
        if not OrderManager.instance:
            OrderManager.instance = OrderManager.__OrderManager()
        return OrderManager.instance

    # pylint: disable=too-many-arguments


