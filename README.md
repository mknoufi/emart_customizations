### EMart Customizations

A comprehensive e-commerce and POS system customization app for Frappe/ERPNext.

## Features

### Product Discount Calculator

A powerful discount calculation engine that supports:

- **Multiple Discount Types**: Percentage, fixed amount, bulk quantity, and category-based discounts
- **Flexible Rule Configuration**: Easy-to-configure discount rules with various parameters  
- **Cart-level Calculations**: Calculate discounts for individual items or entire shopping carts
- **Input Validation**: Robust validation of discount parameters and cart items
- **Maximum Discount Limits**: Prevent excessive discounts with configurable limits
- **Decimal Precision**: Uses Python's Decimal class for accurate financial calculations

#### Quick Example

```python
from emart_customizations.discount_calculator import (
    DiscountEngine, DiscountRule, DiscountType, CartItem
)
from decimal import Decimal

# Create discount engine
engine = DiscountEngine()

# Add a 10% discount rule
rule = DiscountRule(
    rule_id="SUMMER10",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10.00")
)
engine.add_rule(rule)

# Create a cart item
item = CartItem(
    item_id="PROD001",
    name="Laptop", 
    price=Decimal("999.99"),
    quantity=1
)

# Calculate discount
result = engine.calculate_item_discount(item)
print(f"Final price: ${result.final_amount}")  # $899.99
```

See [discount_calculator/README.md](emart_customizations/discount_calculator/README.md) for detailed documentation.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app emart_customizations
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/emart_customizations
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
