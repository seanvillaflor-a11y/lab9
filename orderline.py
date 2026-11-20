from product import Product


class OrderLine:
    """One line of an order: a product and the quantity requested."""

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product = product
        self.__quantity = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print("  " + str(self.__quantity) + " x " + self.__product.name
              + " @ $" + format(self.__product.price, ".2f")
              + " = $" + format(self.calculate_subtotal(), ".2f"))
