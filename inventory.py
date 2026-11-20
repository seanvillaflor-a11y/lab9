from product import Product
from product_factory import product_from_dict
from supplier import Supplier


class Inventory:
    """Manages a collection of Product objects (aggregation)."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def is_empty(self) -> bool:
        return len(self.__products) == 0

    def count(self) -> int:
        return len(self.__products)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.")
            return False
        if product.update_stock(new_stock):
            print("Stock updated successfully!")
            return True
        return False

    def search_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.")
            return None
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print("  Fulfilment: " + product.get_fulfilment_info())
        print("-" * 48)
        return product

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        if self.is_empty():
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def to_list(self) -> list[dict]:
        return [product.to_dict() for product in self.__products]

    def load_from_list(self, data: list[dict],
                       suppliers: dict[str, "Supplier"]) -> None:
        if not isinstance(data, list):
            raise ValueError("inventory data must be a list")
        for item in data:
            supplier = suppliers.get(item.get("supplier_id"))
            if supplier is None:
                raise ValueError(
                    "unknown supplier_id for product " + str(item.get("id")))
            self.add_product(product_from_dict(item, supplier))
