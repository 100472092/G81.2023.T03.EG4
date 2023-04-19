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

    @staticmethod
    def save_orders_shipped(shipment):
        """Saves the shipping object into a file"""
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shimpents_store_file, "r", encoding="utf-8", newline="") as file:
                shipments_store_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            shipments_store_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # append the shipments list
        shipments_store_list.append(shipment.__dict__)

        try:
            with open(shimpents_store_file, "w", encoding="utf-8", newline="") as file:
                json.dump(shipments_store_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    def save_shipments_delivered(self, tracking_code):
        shipments_file = JSON_FILES_PATH + "shipments_delivered.json"
        try:
            with open(shipments_file, "r", encoding="utf-8", newline="") as file:
                shipments_data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found , so  init my data_list
            shipments_data = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # append the delivery info
        shipments_data.append(str(tracking_code))
        shipments_data.append(str(datetime.utcnow()))
        try:
            with open(shipments_file, "w", encoding="utf-8", newline="") as file:
                json.dump(shipments_data, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

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
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # check all the information

        self.validate_dict_attr(data, "OrderID", r"[0-9a-fA-F]{32}$", "Bad label", "order id is not valid")
        self.validate_dict_attr(data, "ContactEmail", r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$', "Bad label",
                                "contact email is not valid")

        proid, reg_type = self.getting_attr_from_order_store(data)

        my_sign = OrderShipping(product_id=proid,
                                order_id=data["OrderID"],
                                order_type=reg_type,
                                delivery_email=data["ContactEmail"])

        # save the OrderShipping in shipments_store.json

        self.save_orders_shipped(my_sign)

        return my_sign.tracking_code

    def validate_attr(self, order_type,regex,mesage):
        myregex = re.compile(regex)
        regex_match = myregex.fullmatch(order_type)
        if not regex_match:
            raise OrderManagementException(mesage)
    def validate_dict_attr(self, dicci, key, regex, message_key_error, message):
        """validates dicctionary data"""
        try:
            self.validate_attr(dicci[key], regex, message)
        except KeyError as ex:
            raise OrderManagementException(message_key_error) from ex

    def getting_attr_from_order_store(self, data):
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

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)

        # check if this tracking_code is in shipments_store
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shimpents_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        # search this tracking_code
        found = False
        for shipment in data_list:
            if shipment["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                del_timestamp = shipment["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")

        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        self.save_shipments_delivered(tracking_code)
        return True
