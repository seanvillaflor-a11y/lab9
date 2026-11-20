from product import Product
from orderline import OrderLine
from discount import DiscountStrategy, NoDiscount


class Order:
    """A customer order, composed of OrderLine objects (composition).

    Strategy pattern: an Order is GIVEN a DiscountStrategy; it does not decide
    the discount itself and contains no if/elif discount logic. If no strategy
    is supplied it uses NoDiscount(). The strategy can be swapped at run time
    with set_discount(). calculate_total() sums the line subtotals and hands
    the result to the strategy's apply() method.

    Order and DiscountStrategy are an association: the order USES a strategy;
    the strategy is not a part of the order and can be shared between orders.
    Multiplicity: Order 1 ---- uses ---- 1 DiscountStrategy; one strategy
    object may back many orders (0..*).
    """

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount strategy on an existing order."""
        self.__discount = discount

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
        """Sum the subtotals, then let the strategy apply itself (no if/elif)."""
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print("Order: " + self.__order_id)
        print("-" * 48)
        if len(self.__order_lines) == 0:
            print("  (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("  Order Total: $" + format(self.calculate_total(), ".2f"))
        print("-" * 48)
