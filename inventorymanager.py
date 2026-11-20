import json
import os
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier
from order import Order
from discount import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.json")


def build_supplier_registry(supplier_dicts: list[dict]) -> dict[str, Supplier]:
    registry: dict[str, Supplier] = {}
    for item in supplier_dicts:
        supplier = Supplier(item["supplier_id"], item["name"], item["contact_email"])
        registry[supplier.supplier_id] = supplier
    return registry


def load_data() -> "tuple[Inventory, dict[str, Supplier]] | None":
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
        suppliers = build_supplier_registry(data.get("suppliers", []))
        inventory = Inventory()
        inventory.load_from_list(data.get("products", []), suppliers)
        print(INVENTORY_FILE + " found.")
        print("Inventory loaded successfully.")
        return inventory, suppliers
    except FileNotFoundError:
        print(INVENTORY_FILE + " not found.")
        return None
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
        print("Could not read " + INVENTORY_FILE + " (" + str(error) + ").")
        backup = INVENTORY_FILE + ".bak"
        try:
            os.replace(INVENTORY_FILE, backup)
            print("The unreadable file was kept as " + backup + ".")
        except OSError:
            pass
        return None


def save_data(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    print("Saving inventory...")
    try:
        os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
        payload = {
            "suppliers": [s.to_dict() for s in suppliers.values()],
            "products": inventory.to_list(),
        }
        with open(INVENTORY_FILE, "w") as file:
            json.dump(payload, file, indent=4)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
        return True
    except OSError as error:
        print("Error saving inventory: " + str(error))
        return False


def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_int(prompt: str) -> int:
    while True:
        try:
            value = int(float(input(prompt)))
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_supplier(suppliers: dict[str, Supplier]) -> "Supplier | None":
    print("Available suppliers:")
    if len(suppliers) == 0:
        print("  (none yet)")
    for supplier in suppliers.values():
        print("  - " + supplier.supplier_id + ": " + supplier.name)
    print("Enter a supplier ID to use, or 'new' to add one.")
    choice = input("Supplier: ").strip()
    if choice.lower() == "new":
        return register_supplier(suppliers)
    supplier = suppliers.get(choice)
    if supplier is None:
        print("No supplier with that ID.")
        return None
    return supplier


def register_supplier(suppliers: dict[str, Supplier]) -> "Supplier | None":
    supplier_id = input("New Supplier ID: ").strip()
    if supplier_id == "":
        print("Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        print("Supplier ID already exists.")
        return None
    name = input("Supplier Name: ").strip()
    if name == "":
        print("Supplier name cannot be empty.")
        return None
    contact_email = input("Supplier Contact Email: ").strip()
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers[supplier_id] = supplier
    print("Supplier added.")
    return supplier


def handle_add(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Product name cannot be empty.")
        return
    price = get_positive_float("Price: ")
    stock = get_int("Stock Quantity: ")

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("A valid supplier is required. Product not added.")
        return

    print("Product type:")
    print("  1. Physical product (has weight, can be shipped)")
    print("  2. Digital product (has download size)")
    type_choice = input("Choose product type (1-2): ").strip()

    if type_choice == "1":
        extra = get_float("Weight (kg): ")
        product_type = "physical"
    elif type_choice == "2":
        extra = get_float("Download size (MB): ")
        product_type = "digital"
    else:
        print("Invalid product type. Product not added.")
        return

    try:
        product = ProductFactory.create(
            product_type, product_id, name, price, stock, supplier, extra)
    except ValueError as error:
        print("Could not create product: " + str(error))
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def handle_update(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print("Name: " + product.name)
    print("Current Stock: " + str(product.stock))
    new_stock = get_int("New Stock Quantity: ")
    inventory.update_stock(product_id, new_stock)


def handle_search(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    inventory.search_product(product_id)


def pick_discount():
    print("Discount:")
    print("  1. None")
    print("  2. Percentage")
    print("  3. Bulk (amount off above a threshold)")
    print("  4. Student (5% off)")
    choice = input("Choose discount (1-4): ").strip()
    if choice == "2":
        return PercentageDiscount(get_positive_float("Percentage off: "))
    if choice == "3":
        threshold = get_positive_float("Threshold: ")
        amount = get_positive_float("Amount off: ")
        return BulkDiscount(threshold, amount)
    if choice == "4":
        return StudentDiscount()
    return NoDiscount()


def handle_order(inventory: Inventory) -> None:
    print("New Order")
    order = Order(input("Order ID: ").strip() or "ORD")
    while True:
        product_id = input("Product ID to add (blank to finish): ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_int("Quantity: ")
        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print("Could not add line: " + str(error))
    order.set_discount(pick_discount())
    order.display_information()


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Create Order")
    print("6. Save Inventory")
    print("7. Exit")
    print("----------------------------")


def create_starter_data() -> "tuple[Inventory, dict[str, Supplier]]":
    suppliers: dict[str, Supplier] = {
        "S001": Supplier("S001", "TechWorld", "sales@techworld.com"),
        "S002": Supplier("S002", "SoftByte", "support@softbyte.com"),
    }
    inventory = Inventory()
    inventory.add_product(
        ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, suppliers["S001"], 2.1))
    inventory.add_product(
        ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, suppliers["S001"], 0.1))
    inventory.add_product(
        ProductFactory.create("digital", "P003", "Antivirus License", 45.00, 25, suppliers["S002"], 350.0))
    return inventory, suppliers


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    loaded = load_data()
    if loaded is None:
        inventory, suppliers = create_starter_data()
        print("Loaded starter suppliers and products.")
        save_data(inventory, suppliers)
    else:
        inventory, suppliers = loaded

    print_menu()

    while True:
        try:
            option = input("Enter option: ").strip()
        except EOFError:
            option = "7"

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory, suppliers)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            handle_order(inventory)
        elif option == "6":
            save_data(inventory, suppliers)
        elif option == "7":
            print("Saving inventory before exit...")
            save_data(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()
