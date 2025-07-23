#!/usr/bin/env python3
"""
Example script demonstrating the Product Discount Calculator functionality.

This script shows how to use the discount calculator for various common
e-commerce scenarios.
"""

from emart_customizations.discount_calculator import (
	DiscountEngine, DiscountRule, DiscountType, CartItem, ValidationError
)
from decimal import Decimal


def print_separator(title: str):
	"""Print a section separator."""
	print(f"\n{'='*60}")
	print(f" {title}")
	print('='*60)


def print_result(result, description: str):
	"""Print discount calculation result."""
	print(f"\n{description}:")
	print(f"  Original Amount: ${result.original_amount}")
	print(f"  Discount Amount: ${result.discount_amount}")
	print(f"  Final Amount: ${result.final_amount}")
	print(f"  Applied Rules: {', '.join(result.applied_rules) or 'None'}")


def main():
	"""Run discount calculator examples."""
	print("Product Discount Calculator - Example Usage")
	
	# Create discount engine
	engine = DiscountEngine()
	
	print_separator("Setting Up Discount Rules")
	
	# Create various discount rules
	rules = [
		DiscountRule(
			rule_id="SUMMER10",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("10.00"),
			description="Summer sale - 10% off everything"
		),
		DiscountRule(
			rule_id="FIXED5",
			discount_type=DiscountType.FIXED_AMOUNT,
			value=Decimal("5.00"),
			description="$5 off per item"
		),
		DiscountRule(
			rule_id="BULK20",
			discount_type=DiscountType.BULK_QUANTITY,
			value=Decimal("20.00"),
			min_quantity=5,
			description="20% off when buying 5 or more"
		),
		DiscountRule(
			rule_id="ELECTRONICS15",
			discount_type=DiscountType.CATEGORY,
			value=Decimal("15.00"),
			category="electronics",
			description="15% off all electronics"
		),
		DiscountRule(
			rule_id="BOOKS25",
			discount_type=DiscountType.CATEGORY,
			value=Decimal("25.00"),
			category="books",
			max_discount=Decimal("20.00"),
			description="25% off books (max $20 discount)"
		)
	]
	
	# Add rules to engine
	for rule in rules:
		engine.add_rule(rule)
		print(f"✓ Added rule: {rule.rule_id} - {rule.description}")
	
	print_separator("Sample Products")
	
	# Create sample products
	products = [
		CartItem(
			item_id="LAPTOP001",
			name="Gaming Laptop",
			price=Decimal("999.99"),
			quantity=1,
			category="electronics"
		),
		CartItem(
			item_id="BOOK001",
			name="Python Programming Guide",
			price=Decimal("49.99"),
			quantity=2,
			category="books"
		),
		CartItem(
			item_id="TSHIRT001",
			name="Cotton T-Shirt",
			price=Decimal("19.99"),
			quantity=6,
			category="clothing"
		),
		CartItem(
			item_id="PHONE001",
			name="Smartphone",
			price=Decimal("599.99"),
			quantity=1,
			category="electronics"
		)
	]
	
	for product in products:
		print(f"• {product.name}: ${product.price} x {product.quantity} ({product.category})")
	
	print_separator("Individual Item Discounts")
	
	# Calculate discounts for individual items
	for product in products:
		result = engine.calculate_item_discount(product)
		print_result(result, f"{product.name}")
	
	print_separator("Shopping Cart Total")
	
	# Calculate total cart discount
	cart_result = engine.calculate_cart_discount(products)
	print_result(cart_result, "Complete Shopping Cart")
	
	# Calculate savings
	savings_percentage = (cart_result.discount_amount / cart_result.original_amount) * 100
	print(f"\nTotal Savings: {savings_percentage:.1f}%")
	
	print_separator("Validation Examples")
	
	# Show validation in action
	try:
		# Try to create invalid item
		invalid_item = CartItem(
			item_id="",  # Empty ID
			name="Invalid Product",
			price=Decimal("10.00"),
			quantity=1
		)
		from emart_customizations.discount_calculator import validate_cart_item
		validate_cart_item(invalid_item)
	except ValidationError as e:
		print(f"✓ Validation caught error: {e}")
	
	try:
		# Try to create invalid rule
		invalid_rule = DiscountRule(
			rule_id="INVALID",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("150.00")  # Over 100%
		)
		from emart_customizations.discount_calculator import validate_discount_rule
		validate_discount_rule(invalid_rule)
	except ValidationError as e:
		print(f"✓ Validation caught error: {e}")
	
	print_separator("Advanced Features")
	
	# Demonstrate rule removal
	print("Removing FIXED5 rule...")
	removed = engine.remove_rule("FIXED5")
	print(f"Rule removed: {removed}")
	
	# Recalculate one item to show difference
	laptop_result_after = engine.calculate_item_discount(products[0])
	print_result(laptop_result_after, "Gaming Laptop (after removing FIXED5 rule)")
	
	print("\n" + "="*60)
	print(" Example completed successfully!")
	print("="*60)


if __name__ == "__main__":
	main()