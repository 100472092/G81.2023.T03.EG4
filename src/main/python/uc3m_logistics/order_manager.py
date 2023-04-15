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

class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_ean13( ean13 ):
        """method vor validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        checksum = 0
        code_read = -1
        res = False
        regex_ean13 = re.compile("^[0-9]{13}$")
        valid_ean13_format = regex_ean13.fullmatch(ean13)
        if valid_ean13_format is None:
            raise OrderManagementException("Invalid EAN13 code string")

        for i, digit in enumerate(reversed(ean13)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            res = True
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return res

    @staticmethod
    def validate_tracking_code( t_c ):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        regex_match = myregex.fullmatch(t_c)
        if not regex_match:
            raise OrderManagementException("tracking_code format is not valid")

    @staticmethod
    def save_order_id(data):
        """Medthod for saving the orders store"""
        file_store = JSON_FILES_PATH + "orders_store.json"
        #first read the file
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                orders_store_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            orders_store_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        found = False
        for order in orders_store_list:
            if order["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            orders_store_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(orders_store_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex
        return True

    @staticmethod
    def save_orders_shipped( shipment ):
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

        #append the shipments list
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
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # append the delivery info
        data_list.append(str(tracking_code))
        data_list.append(str(datetime.utcnow()))
        try:
            with open(shipments_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex



    #pylint: disable=too-many-arguments
    def register_order( self, product_id,
                        order_type,
                        address,
                        phone_number,
                        zip_code ):
        """Register the orders into the order's file"""

        self.validate_attr(order_type,r"(Regular|Premium)","order_type is not valid")
        self.validate_attr(address, r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$", "address is not valid")
        self.validate_attr(phone_number, r"^(\+)[0-9]{11}", "phone number is not valid")

        if zip_code.isnumeric() and len(zip_code) == 5:
            if (int(zip_code) > 52999 or int(zip_code) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)

        self.save_order_id(my_order)

        return my_order.order_id

    def validate_attr(self, order_type,regex,mesage):
        myregex = re.compile(regex)
        regex_match = myregex.fullmatch(order_type)
        if not regex_match:
            raise OrderManagementException(mesage)

    #pylint: disable=too-many-locals
    def send_product ( self, input_file ):
        """Sends the order included in the input_file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        #check all the information
        try:
            self.validate_attr(data["OrderID"],r"[0-9a-fA-F]{32}$","order id is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        try:
            self.validate_attr(data["ContactEmail"],r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$',"contact email is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

        file_store = JSON_FILES_PATH + "orders_store.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for order in data_list:
            if order["_OrderRequest__order_id"] == data["OrderID"]:
                found = True
                #retrieve the orders data
                proid = order["_OrderRequest__product_id"]
                address = order["_OrderRequest__delivery_address"]
                reg_type = order["_OrderRequest__order_type"]
                phone = order["_OrderRequest__phone_number"]
                order_timestamp = order["_OrderRequest__time_stamp"]
                zip_code = order["_OrderRequest__zip_code"]
                #set the time when the order was registered for checking the md5
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

        my_sign= OrderShipping(product_id=proid,
                               order_id=data["OrderID"],
                               order_type=reg_type,
                               delivery_email=data["ContactEmail"])

        #save the OrderShipping in shipments_store.json

        self.save_orders_shipped(my_sign)

        return my_sign.tracking_code

    def deliver_product( self, tracking_code ):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)

        #check if this tracking_code is in shipments_store
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shimpents_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        #search this tracking_code
        found = False
        for shipment in data_list:
            if shipment["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                del_timestamp = shipment["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")

        today= datetime.today().date()
        delivery_date= datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        self.save_shipments_delivered(tracking_code)
        return True

