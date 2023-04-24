"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_manager_config import JSON_FILES_PATH
from .json_op_orders_store import Json_op_order_store
from .json_op_orders_shiped import Json_op_order_shiped
from .json_op_orders_delivered import Json_op_order_delivered
class OrderManager:
    """Class for providing the methods for managing the orders process"""

    def __init__(self):
        pass

    @staticmethod
    def validate_tracking_code(t_c):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        regex_match = myregex.fullmatch(t_c)
        if not regex_match:
            raise OrderManagementException("tracking_code format is not valid")

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
        store = Json_op_order_store()
        store.save_order_id(my_order)
        return my_order.order_id

    # pylint: disable=too-many-locals
    def send_product(self, input_file):
        """Sends the order included in the input_file"""
        #data = self.read_json_file(input_file)

        # check all the information

        #self.validate_dict_attr(data, "OrderID", r"[0-9a-fA-F]{32}$", "Bad label", "order id is not valid")
        #self.validate_dict_attr(data, "ContactEmail", r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$', "Bad label",
                                #"contact email is not valid")

        #proid, reg_type = self.getting_attr_from_order_store(data)

        my_sign = OrderShipping(input_file)

        # save the OrderShipping in shipments_store.json
        store = Json_op_order_shiped()
        store.save_shipments_delivered(my_sign)
        return my_sign.tracking_code

    def read_json_file(self, input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    """def validate_attr(self, order_type,regex,mesage):
        myregex = re.compile(regex)
        regex_match = myregex.fullmatch(order_type)
        if not regex_match:
            raise OrderManagementException(mesage)"""
    """def validate_dict_attr(self, dicci, key, regex, message_key_error, message):
        try:
            self.validate_attr(dicci[key], regex, message)
        except KeyError as ex:
            raise OrderManagementException(message_key_error) from ex
"""
    """def getting_attr_from_order_store(self, data):
        file_store = JSON_FILES_PATH + "orders_store.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for order in data_list:
            if order["_OrderRequest__order_id"] == data["OrderID"]:
                found = True
                # retrieve the orders data
                proid = order["_OrderRequest__product_id"]
                address = order["_OrderRequest__delivery_address"]
                reg_type = order["_OrderRequest__order_type"]
                phone = order["_OrderRequest__phone_number"]
                order_timestamp = order["_OrderRequest__time_stamp"]
                zip_code = order["_OrderRequest__zip_code"]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=proid,
                                         delivery_address=address,
                                         order_type=reg_type,
                                         phone_number=phone,
                                         zip_code=zip_code)

                if order.order_id != data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")
        if not found:
            raise OrderManagementException("order_id not found")
        return proid, reg_type
"""
    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)

        #del_timestamp = self.check_tracking_code(tracking_code)
        del_timestamp = Json_op_order_delivered().check_tracking_code(tracking_code)
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        store = Json_op_order_delivered()
        store.save_shipments_delivered(tracking_code)
        return True
