import json
from .order_management_exception import OrderManagementException


class Json_op():
    def __init__(self):
        self.path = ""
        self.ip = ""
        self.data_list = None

    def open(self):
        """Medthod for saving the orders store"""
        # first read the file
        try:
            with open(self.path, "r", encoding="utf-8", newline="") as file:
                self.data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            self.data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
    def search(self, value):
        if self.data_list is None:
            self.open()
        for item in self.data_list:
            if item[self.ip] == value:
                return item
        return None
    def save(self):
        if self.data_list is None:
            self.open()
        try:
            with open(self.path, "w", encoding="utf-8", newline="") as file:
                json.dump(self.data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex