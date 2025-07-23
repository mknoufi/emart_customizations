"""Core discount calculation engine and data structures."""

from enum import Enum
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


class DiscountType(Enum):
	"""Types of discounts supported by the system."""
	PERCENTAGE = "percentage"
	FIXED_AMOUNT = "fixed_amount"
	BULK_QUANTITY = "bulk_quantity"
	CATEGORY = "category"


@dataclass
class DiscountRule:
	"""Represents a discount rule configuration."""
	rule_id: str
	discount_type: DiscountType
	value: Decimal
	min_quantity: Optional[int] = None
	category: Optional[str] = None
	max_discount: Optional[Decimal] = None
	description: Optional[str] = None


@dataclass 
class CartItem:
	"""Represents an item in a shopping cart."""
	item_id: str
	name: str
	price: Decimal
	quantity: int
	category: Optional[str] = None


@dataclass
class DiscountResult:
	"""Result of discount calculation."""
	original_amount: Decimal
	discount_amount: Decimal
	final_amount: Decimal
	applied_rules: List[str]


class DiscountEngine:
	"""Main engine for calculating discounts."""
	
	def __init__(self):
		"""Initialize the discount engine."""
		self.rules: List[DiscountRule] = []
	
	def add_rule(self, rule: DiscountRule) -> None:
		"""Add a discount rule to the engine.
		
		Args:
			rule: The discount rule to add
		"""
		self.rules.append(rule)
	
	def remove_rule(self, rule_id: str) -> bool:
		"""Remove a discount rule by ID.
		
		Args:
			rule_id: ID of the rule to remove
			
		Returns:
			True if rule was found and removed, False otherwise
		"""
		initial_count = len(self.rules)
		self.rules = [rule for rule in self.rules if rule.rule_id != rule_id]
		return len(self.rules) < initial_count
	
	def calculate_item_discount(self, item: CartItem, applicable_rules: Optional[List[DiscountRule]] = None) -> DiscountResult:
		"""Calculate discount for a single cart item.
		
		Args:
			item: The cart item to calculate discount for
			applicable_rules: Specific rules to apply (if None, uses all rules)
			
		Returns:
			DiscountResult with calculated discount
		"""
		if applicable_rules is None:
			applicable_rules = self._get_applicable_rules(item)
		
		total_discount = Decimal("0")
		applied_rule_ids = []
		original_amount = item.price * item.quantity
		
		for rule in applicable_rules:
			discount = self._apply_single_rule(item, rule)
			if discount > 0:
				total_discount += discount
				applied_rule_ids.append(rule.rule_id)
		
		# Ensure discount doesn't exceed original amount
		total_discount = min(total_discount, original_amount)
		final_amount = original_amount - total_discount
		
		return DiscountResult(
			original_amount=original_amount,
			discount_amount=total_discount,
			final_amount=final_amount,
			applied_rules=applied_rule_ids
		)
	
	def calculate_cart_discount(self, cart_items: List[CartItem]) -> DiscountResult:
		"""Calculate total discount for entire cart.
		
		Args:
			cart_items: List of items in the cart
			
		Returns:
			DiscountResult with total cart discount
		"""
		total_original = Decimal("0")
		total_discount = Decimal("0")
		all_applied_rules = []
		
		for item in cart_items:
			item_result = self.calculate_item_discount(item)
			total_original += item_result.original_amount
			total_discount += item_result.discount_amount
			all_applied_rules.extend(item_result.applied_rules)
		
		# Remove duplicate rule IDs
		unique_applied_rules = list(set(all_applied_rules))
		
		return DiscountResult(
			original_amount=total_original,
			discount_amount=total_discount,
			final_amount=total_original - total_discount,
			applied_rules=unique_applied_rules
		)
	
	def _get_applicable_rules(self, item: CartItem) -> List[DiscountRule]:
		"""Get rules applicable to a specific item.
		
		Args:
			item: Cart item to check rules for
			
		Returns:
			List of applicable discount rules
		"""
		applicable = []
		
		for rule in self.rules:
			if self._is_rule_applicable(item, rule):
				applicable.append(rule)
		
		return applicable
	
	def _is_rule_applicable(self, item: CartItem, rule: DiscountRule) -> bool:
		"""Check if a rule is applicable to an item.
		
		Args:
			item: Cart item to check
			rule: Discount rule to check
			
		Returns:
			True if rule applies to item
		"""
		# Check quantity requirement
		if rule.min_quantity and item.quantity < rule.min_quantity:
			return False
		
		# Check category requirement
		if rule.category and item.category != rule.category:
			return False
		
		return True
	
	def _apply_single_rule(self, item: CartItem, rule: DiscountRule) -> Decimal:
		"""Apply a single discount rule to an item.
		
		Args:
			item: Cart item to apply discount to
			rule: Discount rule to apply
			
		Returns:
			Discount amount
		"""
		item_total = item.price * item.quantity
		
		if rule.discount_type == DiscountType.PERCENTAGE:
			discount = item_total * (rule.value / Decimal("100"))
		elif rule.discount_type == DiscountType.FIXED_AMOUNT:
			discount = rule.value * item.quantity
		elif rule.discount_type == DiscountType.BULK_QUANTITY:
			if item.quantity >= (rule.min_quantity or 1):
				discount = item_total * (rule.value / Decimal("100"))
			else:
				discount = Decimal("0")
		elif rule.discount_type == DiscountType.CATEGORY:
			if item.category == rule.category:
				discount = item_total * (rule.value / Decimal("100"))
			else:
				discount = Decimal("0")
		else:
			discount = Decimal("0")
		
		# Apply maximum discount limit if specified
		if rule.max_discount and discount > rule.max_discount:
			discount = rule.max_discount
		
		# Round to 2 decimal places
		return discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)