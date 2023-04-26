"""Contains the class OrderShipping"""
# pylint: disable=import-error
from datetime import datetime
import hashlib
import json
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from freezegun import freeze_time
from .order_request import OrderRequest
from .atributo_email import Email
from .atributo_order_id import OrderId


# pylint: disable=too-many-instance-attributes
class OrderShipping():
    """Class representing the shipping of an order"""

    def __init__(self, input_file):
        self.__myorder_id, self.__myemail = self.validate_key_labels(
            self.read_json_file(input_file))
        self.__order_id = OrderId(self.__myorder_id).validate_attr(self.__myorder_id)
        self.__delivery_email = Email(self.__myemail).validate_attr(self.__myemail)
        self.__product_id, self.__order_type = self.getting_attr_from_order_store(
            self.read_json_file(input_file))
        self.__alg = "SHA-256"
        self.__type = "DS"

        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if self.__order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1
        # timestamp is represneted in seconds.microseconds
        # __delivery_day must be expressed in senconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
            self.__order_id + ",issuedate:" + str(self.__issued_at) + \
            ",deliveryday:" + str(self.__delivery_day) + "}"

    def read_json_file(self, input_file):
        """reads data from json"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    def validate_key_labels(self, data):
        """validates the keys we must search for"""
        try:
            order_id = data["OrderID"]
            email = data["ContactEmail"]
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        return order_id, email

    def getting_attr_from_order_store(self, data):
        """gets  attr from order_store"""
        file_store = JSON_FILES_PATH + "orders_store.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for order in data_list:
            if order["_OrderRequest__order_id"] == data["OrderID"]:
                found = True
                # retrieve the orders data
                prod_id = order["_OrderRequest__product_id"]
                address = order["_OrderRequest__delivery_address"]
                reg_type = order["_OrderRequest__order_type"]
                phone = order["_OrderRequest__phone_number"]
                order_timestamp = order["_OrderRequest__time_stamp"]
                zip_code = order["_OrderRequest__zip_code"]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=prod_id,
                                         delivery_address=address,
                                         order_type=reg_type,
                                         phone_number=phone,
                                         zip_code=zip_code)

                if order.order_id != data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")
        if not found:
            raise OrderManagementException("order_id not found")
        return prod_id, reg_type

    @property
    def product_id(self):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def order_id(self):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def email(self):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @email.setter
    def email(self, value):
        self.__delivery_email = value

    @property
    def tracking_code(self):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def delivery_day(self):
        """Returns the delivery day for the order"""
        return self.__delivery_day
