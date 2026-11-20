import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discount import (
    DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount)
from supplier import Supplier
from order import Order


class DiscountStrategyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld", "sales@techworld.com")

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_bulk_discount_applies_above_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)

    def test_bulk_discount_ignored_below_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_student_discount_takes_five_percent(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    def test_order_defaults_to_no_discount(self) -> None:
        self.assertIsInstance(Order("ORD1").discount, NoDiscount)

    def test_order_uses_bulk_then_percentage_after_set_discount(self) -> None:
        from physicalproduct import PhysicalProduct
        product = PhysicalProduct("P001", "Lamp", 125.0, 10, self.supplier, 1.0)
        order = Order("ORD2", BulkDiscount(200, 20))
        order.add_order_line(product, 2)
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_needs_no_change_to_order(self) -> None:
        class RoundDownDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return float(int(total))

        from physicalproduct import PhysicalProduct
        product = PhysicalProduct("P001", "Lamp", 10.5, 10, self.supplier, 1.0)
        order = Order("ORD3", RoundDownDiscount())
        order.add_order_line(product, 1)
        self.assertEqual(order.calculate_total(), 10.0)


if __name__ == "__main__":
    unittest.main()
