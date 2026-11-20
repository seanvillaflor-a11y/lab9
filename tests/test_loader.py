import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "products.csv")


class LoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld", "sales@techworld.com")

    def test_bad_rows_skipped_valid_rows_loaded(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(CSV_PATH, inventory, self.supplier)
        self.assertEqual(inventory.count(), 3)
        self.assertEqual(output.getvalue().count("Skipped bad row"), 2)
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_missing_file_handled_gracefully(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products("does_not_exist.csv", inventory, self.supplier)
        self.assertEqual(inventory.count(), 0)
        self.assertIn("Products file not found", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
