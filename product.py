from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base for all products. Manages common product state.

    Lab 9 validation: a Product owns two rules and enforces them itself -- the
    price must be greater than zero and the stock quantity cannot be negative.
    The checks live here, in the class that owns the data, and raise
    ValueError with a clear message.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock < 0:
            raise ValueError("Product stock quantity cannot be negative.")

        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        """Set the stock to quantity. Rejects negative values (LSP: both
        subclasses inherit this rule unchanged)."""
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print("ID: " + self.__product_id
              + " | Name: " + self.__name
              + " | Price: $" + format(self.__price, ".2f")
              + " | Stock: " + str(self.__stock)
              + " | Supplier: " + self.__supplier.name)

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is fulfilled."""
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.supplier_id,
        }
