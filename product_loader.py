import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def get_positive_float(prompt: str) -> float:
    """Ask for a number greater than zero and keep asking until one is given.

    Exception handling: float() raises ValueError on text like 'abc'.
    Validation: a value of zero or below is rejected. The function never
    continues with bad data; it loops until a valid value is entered.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into the inventory, failing gracefully.

    try / except / else / finally:
      - try opens the file; a missing file raises FileNotFoundError.
      - except FileNotFoundError reports it and does not crash.
      - else (file opened) reads each row inside its own try/except ValueError,
        so one bad row is reported and skipped while loading carries on.
      - finally always runs, reporting that the load attempt is finished.
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print("Products file not found: " + path)
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                if not row:
                    continue
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        float(price), int(stock_quantity), supplier)
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print("Skipped duplicate product id: " + product_id)
                except ValueError as error:
                    print("Skipped bad row " + str(row) + " (" + str(error) + ").")
        print(str(loaded) + " products loaded.")
    finally:
        print("Load attempt finished.")
