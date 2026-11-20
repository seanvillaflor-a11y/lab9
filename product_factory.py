from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Factory pattern: one place that owns how products are created.

    Without the factory, every part of the program that needs a product must
    know about PhysicalProduct and DigitalProduct directly and must change
    when a new type is added. With the factory, callers ask for a Product by a
    type string and receive a Product (the base type).

    The factory itself still has an if/elif and must change when a new type is
    added, so it does not fully satisfy OCP. That is acceptable for a small
    application: the change is isolated to this single method.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, extra: float = 0.0) -> Product:
        """Create and return a Product of the requested type.

        'extra' is weight (kg) for a physical product, or download size (MB)
        for a digital product. An unknown type raises ValueError.
        """
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra)
        if product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra)
        raise ValueError("Unknown product type: " + str(product_type))


def product_from_dict(data: dict, supplier: Supplier) -> Product:
    """Build the correct Product subclass from a saved dictionary.

    Delegates the actual creation to ProductFactory so there is a single place
    that knows the concrete product classes.
    """
    product_type = data.get("type", "physical")
    extra = data.get("download_size", 0.0) if product_type == "digital" \
        else data.get("weight", 0.0)

    return ProductFactory.create(
        product_type, data["id"], data["name"], data["price"],
        data["stock"], supplier, extra)
