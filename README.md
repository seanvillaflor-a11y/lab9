# INF1103 Lab 9 - Design Patterns and Error Handling

Builds on Lab 8. Adds the Strategy pattern (order discounts), the Factory
pattern (product creation), validation, exception handling and automated tests.

## What is new in Lab 9

- **Strategy pattern** (`discount.py`): `DiscountStrategy` ABC with `NoDiscount`,
  `PercentageDiscount`, `BulkDiscount` and `StudentDiscount`. `Order` is given a
  strategy and contains no discount if/elif logic; it can be swapped with
  `set_discount()`.
- **Factory pattern** (`product_factory.py`): `ProductFactory.create()` is the
  single place that knows the concrete product classes and returns a `Product`.
- **Validation**: price > 0 and stock >= 0 in `Product`; quantity > 0 in
  `OrderLine`.
- **Exception handling** (`product_loader.py`): `get_positive_float()` and
  `load_products()` using try / except / else / finally.
- **Automated tests** (`tests/`): cover the strategies, factory, validation and
  the file loader.

## Run

```
python inventorymanager.py
```

## Run the tests

```
python -m unittest discover -s tests -v
```

## Docker

```
docker build -t inf1103-lab9 .
docker run -it --rm -v "$(pwd)/data:/app/data" inf1103-lab9
```
