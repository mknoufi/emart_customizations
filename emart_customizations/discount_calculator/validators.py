"""Input validation utilities for discount calculator."""

from typing import Optional, List
from decimal import Decimal

from .discount_engine import CartItem, DiscountRule, DiscountType


class ValidationError(Exception):
	"""Custom exception for validation errors."""
	pass


def validate_cart_item(item: CartItem) -> None:
	"""Validate a cart item.
	
	Args:
		item: Cart item to validate
		
	Raises:
		ValidationError: If item is invalid
	"""
	if not isinstance(item, CartItem):
		raise ValidationError("Item must be a CartItem instance")
	
	if not item.item_id or not isinstance(item.item_id, str):
		raise ValidationError("Item ID must be a non-empty string")
	
	if not item.name or not isinstance(item.name, str):
		raise ValidationError("Item name must be a non-empty string")
	
	if not isinstance(item.price, Decimal) or item.price < 0:
		raise ValidationError("Item price must be a non-negative Decimal")
	
	if not isinstance(item.quantity, int) or item.quantity <= 0:
		raise ValidationError("Item quantity must be a positive integer")
	
	if item.category is not None and not isinstance(item.category, str):
		raise ValidationError("Item category must be a string or None")


def validate_discount_rule(rule: DiscountRule) -> None:
	"""Validate a discount rule.
	
	Args:
		rule: Discount rule to validate
		
	Raises:
		ValidationError: If rule is invalid
	"""
	if not isinstance(rule, DiscountRule):
		raise ValidationError("Rule must be a DiscountRule instance")
	
	if not rule.rule_id or not isinstance(rule.rule_id, str):
		raise ValidationError("Rule ID must be a non-empty string")
	
	if not isinstance(rule.discount_type, DiscountType):
		raise ValidationError("Discount type must be a valid DiscountType")
	
	if not isinstance(rule.value, Decimal) or rule.value < 0:
		raise ValidationError("Rule value must be a non-negative Decimal")
	
	# Percentage discounts shouldn't exceed 100%
	if rule.discount_type in [DiscountType.PERCENTAGE, DiscountType.BULK_QUANTITY, DiscountType.CATEGORY]:
		if rule.value > Decimal("100"):
			raise ValidationError("Percentage discount cannot exceed 100%")
	
	if rule.min_quantity is not None:
		if not isinstance(rule.min_quantity, int) or rule.min_quantity <= 0:
			raise ValidationError("Minimum quantity must be a positive integer")
	
	if rule.category is not None and not isinstance(rule.category, str):
		raise ValidationError("Category must be a string or None")
	
	if rule.max_discount is not None:
		if not isinstance(rule.max_discount, Decimal) or rule.max_discount < 0:
			raise ValidationError("Maximum discount must be a non-negative Decimal")
	
	# Rule-specific validations
	if rule.discount_type == DiscountType.BULK_QUANTITY and rule.min_quantity is None:
		raise ValidationError("Bulk quantity discount requires min_quantity")
	
	if rule.discount_type == DiscountType.CATEGORY and rule.category is None:
		raise ValidationError("Category discount requires category")


def validate_cart_items(items: List[CartItem]) -> None:
	"""Validate a list of cart items.
	
	Args:
		items: List of cart items to validate
		
	Raises:
		ValidationError: If any item is invalid
	"""
	if not isinstance(items, list):
		raise ValidationError("Items must be a list")
	
	if not items:
		raise ValidationError("Cart cannot be empty")
	
	item_ids = []
	for i, item in enumerate(items):
		try:
			validate_cart_item(item)
		except ValidationError as e:
			raise ValidationError(f"Item {i}: {str(e)}")
		
		# Check for duplicate item IDs
		if item.item_id in item_ids:
			raise ValidationError(f"Duplicate item ID: {item.item_id}")
		item_ids.append(item.item_id)