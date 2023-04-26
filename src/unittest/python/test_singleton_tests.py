"""Tests singleton"""

# pylint: disable=import-error
from unittest import TestCase
from uc3m_logistics import OrderManager
from uc3m_logistics.store import json_op_orders_delivered
from uc3m_logistics.store import json_op_orders_shiped
from uc3m_logistics.store import json_op_orders_store


class TestDeliverProduct(TestCase):
    """Class for testing deliver_product"""

    def test_singleton_order_manager(self):
        """two instances that must be equal"""
        my_manager = OrderManager()
        my_manager2 = OrderManager()
        self.assertEqual(my_manager, my_manager2)

    def test_singletone_json_order_delivered(self):
        """two instances that must be equal"""
        my_store = json_op_orders_delivered.JsonOpOrderDelivered()
        my_store1 = json_op_orders_delivered.JsonOpOrderDelivered()
        self.assertEqual(my_store, my_store1)

    def test_singletone_json_order_shiped(self):
        """two instances that must be equal"""
        my_store = json_op_orders_shiped.JsonOpOrderShiped()
        my_store1 = json_op_orders_shiped.JsonOpOrderShiped()
        self.assertEqual(my_store, my_store1)

    def test_singletone_json_order_store(self):
        """two instances that must be equal"""
        my_store = json_op_orders_store.JsonOpOrderStore()
        my_store1 = json_op_orders_store.JsonOpOrderStore()
        self.assertEqual(my_store, my_store1)
