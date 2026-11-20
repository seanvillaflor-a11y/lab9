from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


def product_from_dict(data: dict, supplier: Supplier) -> Product:
    """Build the correct Product subclass from a saved dictionary."""
    product_type = data.get("type", "physical")

    if product_type == "digital":
        return DigitalProduct(
            data["id"], data["name"], data["price"], data["stock"],
            supplier, data.get("download_size", 0.0))

    if product_type == "physical":
        return PhysicalProduct(
            data["id"], data["name"], data["price"], data["stock"],
            supplier, data.get("weight", 0.0))

    raise ValueError("Unknown product type: " + str(product_type))
