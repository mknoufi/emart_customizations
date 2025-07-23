# Product Discount Calculator

A comprehensive discount calculation module for e-commerce and POS systems.

## Features

- **Multiple Discount Types**: Supports percentage, fixed amount, bulk quantity, and category-based discounts
- **Flexible Rule Configuration**: Easy-to-configure discount rules with various parameters
- **Cart-level Calculations**: Calculate discounts for individual items or entire shopping carts
- **Input Validation**: Robust validation of discount parameters and cart items
- **Maximum Discount Limits**: Prevent excessive discounts with configurable limits
- **Decimal Precision**: Uses Python's Decimal class for accurate financial calculations

## Quick Start

```python
from emart_customizations.discount_calculator import (
    DiscountEngine, DiscountRule, DiscountType, CartItem
)
from decimal import Decimal

# Create discount engine
engine = DiscountEngine()

# Add a 10% discount rule
percentage_rule = DiscountRule(
    rule_id="SUMMER10",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10.00"),
    description="Summer sale 10% off"
)
engine.add_rule(percentage_rule)

# Create a cart item
item = CartItem(
    item_id="PROD001",
    name="Laptop",
    price=Decimal("999.99"),
    quantity=1,
    category="electronics"
)

# Calculate discount
result = engine.calculate_item_discount(item)
print(f"Original: ${result.original_amount}")
print(f"Discount: ${result.discount_amount}")
print(f"Final: ${result.final_amount}")
```

## Discount Types

### 1. Percentage Discount
Applies a percentage discount to the item total.

```python
rule = DiscountRule(
    rule_id="PERCENT15",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("15.00")  # 15% off
)
```

### 2. Fixed Amount Discount
Applies a fixed dollar amount discount per item.

```python
rule = DiscountRule(
    rule_id="FIXED5",
    discount_type=DiscountType.FIXED_AMOUNT,
    value=Decimal("5.00")  # $5 off per item
)
```

### 3. Bulk Quantity Discount
Applies a percentage discount when minimum quantity is met.

```python
rule = DiscountRule(
    rule_id="BULK20",
    discount_type=DiscountType.BULK_QUANTITY,
    value=Decimal("20.00"),  # 20% off
    min_quantity=5  # when buying 5 or more
)
```

### 4. Category Discount
Applies a percentage discount to items in specific categories.

```python
rule = DiscountRule(
    rule_id="ELECTRONICS25",
    discount_type=DiscountType.CATEGORY,
    value=Decimal("25.00"),  # 25% off
    category="electronics"  # only for electronics
)
```

## Advanced Features

### Maximum Discount Limits
Prevent excessive discounts by setting a maximum discount amount:

```python
rule = DiscountRule(
    rule_id="LIMITED50",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("50.00"),  # 50% off
    max_discount=Decimal("100.00")  # but max $100 discount
)
```

### Cart-level Calculations
Calculate discounts for an entire shopping cart:

```python
cart_items = [item1, item2, item3]
cart_result = engine.calculate_cart_discount(cart_items)
```

### Multiple Rules
Apply multiple discount rules to the same item:

```python
engine.add_rule(percentage_rule)
engine.add_rule(category_rule)
# Both rules will be applied if applicable
```

## Data Structures

### CartItem
Represents an item in a shopping cart:
- `item_id` (str): Unique identifier for the item
- `name` (str): Display name of the item
- `price` (Decimal): Unit price of the item
- `quantity` (int): Number of items
- `category` (str, optional): Item category

### DiscountRule
Represents a discount rule configuration:
- `rule_id` (str): Unique identifier for the rule
- `discount_type` (DiscountType): Type of discount
- `value` (Decimal): Discount value (percentage or amount)
- `min_quantity` (int, optional): Minimum quantity requirement
- `category` (str, optional): Required category
- `max_discount` (Decimal, optional): Maximum discount amount
- `description` (str, optional): Human-readable description

### DiscountResult
Result of discount calculation:
- `original_amount` (Decimal): Original total before discount
- `discount_amount` (Decimal): Total discount applied
- `final_amount` (Decimal): Final total after discount
- `applied_rules` (List[str]): List of rule IDs that were applied

## Validation

The module includes comprehensive validation:

```python
from emart_customizations.discount_calculator import validate_cart_item, ValidationError

try:
    validate_cart_item(item)
    print("Item is valid")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Error Handling

The module provides custom exceptions for better error handling:

- `ValidationError`: Raised when input validation fails

## Best Practices

1. **Use Decimal for Money**: Always use Python's `Decimal` class for monetary values to avoid floating-point precision issues.

2. **Validate Inputs**: Always validate cart items and discount rules before processing.

3. **Set Maximum Limits**: Consider setting maximum discount limits to prevent abuse.

4. **Test Edge Cases**: Test with zero quantities, negative prices, and extreme discount values.

5. **Rule Ordering**: Be aware that rules are applied in the order they were added to the engine.

## Examples

### Basic E-commerce Discount
```python
# 10% off orders over $100
rule = DiscountRule(
    rule_id="ORDER100",
    discount_type=DiscountType.PERCENTAGE,
    value=Decimal("10.00"),
    min_quantity=1,
    description="10% off orders over $100"
)

# Note: You would need to check order total separately
# This rule applies to individual items
```

### Buy-More-Save-More
```python
# 15% off when buying 3 or more of the same item
bulk_rule = DiscountRule(
    rule_id="BUY3SAVE15",
    discount_type=DiscountType.BULK_QUANTITY,
    value=Decimal("15.00"),
    min_quantity=3
)
```

### Category Sale
```python
# 30% off all books
books_rule = DiscountRule(
    rule_id="BOOKS30",
    discount_type=DiscountType.CATEGORY,
    value=Decimal("30.00"),
    category="books"
)
```

### Clearance Sale
```python
# $10 off per item, but maximum $50 discount
clearance_rule = DiscountRule(
    rule_id="CLEARANCE",
    discount_type=DiscountType.FIXED_AMOUNT,
    value=Decimal("10.00"),
    max_discount=Decimal("50.00")
)
```