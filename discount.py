from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: the interchangeable 'how to discount a total' behaviour.

    Each way of discounting an order total lives in its own class. Every
    strategy provides the same method, apply(), so the Order that uses a
    strategy only calls apply() and never needs to know which concrete
    strategy it holds.
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total for the given order total."""
        raise NotImplementedError


class NoDiscount(DiscountStrategy):
    """Default strategy: return the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Take a fixed percentage off the total. e.g. PercentageDiscount(10)."""

    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Take a flat amount off once the total reaches a threshold.

    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more.
    """

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold = threshold
        self.__amount = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy (Section 2.4): a flat 5% student discount.

    Added without changing Order at all -- Order still just calls apply().
    This is the point of the Strategy pattern: new behaviour, no edits to the
    class that uses it.
    """

    STUDENT_RATE: float = 5.0

    def apply(self, total: float) -> float:
        return total * (1 - StudentDiscount.STUDENT_RATE / 100)
