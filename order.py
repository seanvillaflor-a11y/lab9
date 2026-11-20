from product import Product
from orderline import OrderLine


class Order:
    """A customer order, composed of OrderLine objects (composition)."""

    def __init__(self, order_id: str) -> None:
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print("Order: " + self.__order_id)
        print("-" * 48)
        if len(self.__order_lines) == 0:
            print("  (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("  Order Total: $" + format(self.calculate_total(), ".2f"))
        print("-" * 48)
