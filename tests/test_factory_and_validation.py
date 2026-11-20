import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from product_factory import ProductFactory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from product import Product
from orderline import OrderLine
from supplier import Supplier


class FactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld", "sales@techworld.com")

    def test_factory_creates_physical(self) -> None:
        product = ProductFactory.create(
            "physical", "P001", "Lamp", 25.0, 10, self.supplier, 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_factory_creates_digital(self) -> None:
        product = ProductFactory.create(
            "digital", "D001", "Editor", 49.9, 100, self.supplier, 350.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S001", "Install", 30.0, 5, self.supplier)


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld", "sales@techworld.com")

    def test_zero_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Lamp", 0.0, 10, self.supplier, 1.0)

    def test_negative_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DigitalProduct("D001", "Editor", -5.0, 10, self.supplier, 10.0)

    def test_negative_stock_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Lamp", 10.0, -1, self.supplier, 1.0)

    def test_order_line_quantity_must_be_positive(self) -> None:
        product = PhysicalProduct("P001", "Lamp", 10.0, 10, self.supplier, 1.0)
        with self.assertRaises(ValueError):
            OrderLine(product, 0)


if __name__ == "__main__":
    unittest.main()
