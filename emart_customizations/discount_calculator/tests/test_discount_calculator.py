"""Unit tests for the discount calculator module."""

import unittest
from decimal import Decimal

from ..discount_engine import (
	DiscountEngine, DiscountRule, DiscountType, CartItem, DiscountResult
)
from ..validators import validate_cart_item, validate_discount_rule, ValidationError


class TestDiscountEngine(unittest.TestCase):
	"""Test cases for DiscountEngine class."""
	
	def setUp(self):
		"""Set up test fixtures."""
		self.engine = DiscountEngine()
		
		# Sample cart items
		self.item1 = CartItem(
			item_id="ITEM001",
			name="Test Product 1",
			price=Decimal("10.00"),
			quantity=2,
			category="electronics"
		)
		
		self.item2 = CartItem(
			item_id="ITEM002", 
			name="Test Product 2",
			price=Decimal("25.00"),
			quantity=5,
			category="books"
		)
		
		# Sample discount rules
		self.percentage_rule = DiscountRule(
			rule_id="PERCENT10",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("10.00"),
			description="10% off everything"
		)
		
		self.fixed_rule = DiscountRule(
			rule_id="FIXED5",
			discount_type=DiscountType.FIXED_AMOUNT,
			value=Decimal("5.00"),
			description="$5 off per item"
		)
		
		self.bulk_rule = DiscountRule(
			rule_id="BULK20",
			discount_type=DiscountType.BULK_QUANTITY,
			value=Decimal("20.00"),
			min_quantity=5,
			description="20% off for 5+ items"
		)
		
		self.category_rule = DiscountRule(
			rule_id="ELECTRONICS15",
			discount_type=DiscountType.CATEGORY,
			value=Decimal("15.00"),
			category="electronics",
			description="15% off electronics"
		)
	
	def test_add_remove_rules(self):
		"""Test adding and removing discount rules."""
		# Initially empty
		self.assertEqual(len(self.engine.rules), 0)
		
		# Add rule
		self.engine.add_rule(self.percentage_rule)
		self.assertEqual(len(self.engine.rules), 1)
		
		# Remove rule
		result = self.engine.remove_rule("PERCENT10")
		self.assertTrue(result)
		self.assertEqual(len(self.engine.rules), 0)
		
		# Try to remove non-existent rule
		result = self.engine.remove_rule("NONEXISTENT")
		self.assertFalse(result)
	
	def test_percentage_discount(self):
		"""Test percentage-based discount calculation."""
		self.engine.add_rule(self.percentage_rule)
		
		result = self.engine.calculate_item_discount(self.item1)
		
		# Original: 10.00 * 2 = 20.00
		# 10% discount: 2.00
		# Final: 18.00
		self.assertEqual(result.original_amount, Decimal("20.00"))
		self.assertEqual(result.discount_amount, Decimal("2.00"))
		self.assertEqual(result.final_amount, Decimal("18.00"))
		self.assertIn("PERCENT10", result.applied_rules)
	
	def test_fixed_amount_discount(self):
		"""Test fixed amount discount calculation."""
		self.engine.add_rule(self.fixed_rule)
		
		result = self.engine.calculate_item_discount(self.item1)
		
		# Original: 10.00 * 2 = 20.00
		# Fixed discount: 5.00 * 2 = 10.00
		# Final: 10.00
		self.assertEqual(result.original_amount, Decimal("20.00"))
		self.assertEqual(result.discount_amount, Decimal("10.00"))
		self.assertEqual(result.final_amount, Decimal("10.00"))
		self.assertIn("FIXED5", result.applied_rules)
	
	def test_bulk_quantity_discount(self):
		"""Test bulk quantity discount calculation."""
		self.engine.add_rule(self.bulk_rule)
		
		# Test with item that meets minimum quantity
		result = self.engine.calculate_item_discount(self.item2)
		
		# Original: 25.00 * 5 = 125.00
		# Bulk discount (20%): 25.00
		# Final: 100.00
		self.assertEqual(result.original_amount, Decimal("125.00"))
		self.assertEqual(result.discount_amount, Decimal("25.00"))
		self.assertEqual(result.final_amount, Decimal("100.00"))
		self.assertIn("BULK20", result.applied_rules)
		
		# Test with item that doesn't meet minimum quantity
		result = self.engine.calculate_item_discount(self.item1)
		
		# No discount should be applied
		self.assertEqual(result.original_amount, Decimal("20.00"))
		self.assertEqual(result.discount_amount, Decimal("0.00"))
		self.assertEqual(result.final_amount, Decimal("20.00"))
		self.assertNotIn("BULK20", result.applied_rules)
	
	def test_category_discount(self):
		"""Test category-specific discount calculation."""
		self.engine.add_rule(self.category_rule)
		
		# Test with electronics item
		result = self.engine.calculate_item_discount(self.item1)
		
		# Original: 10.00 * 2 = 20.00
		# Category discount (15%): 3.00
		# Final: 17.00
		self.assertEqual(result.original_amount, Decimal("20.00"))
		self.assertEqual(result.discount_amount, Decimal("3.00"))
		self.assertEqual(result.final_amount, Decimal("17.00"))
		self.assertIn("ELECTRONICS15", result.applied_rules)
		
		# Test with non-electronics item
		result = self.engine.calculate_item_discount(self.item2)
		
		# No discount should be applied
		self.assertEqual(result.original_amount, Decimal("125.00"))
		self.assertEqual(result.discount_amount, Decimal("0.00"))
		self.assertEqual(result.final_amount, Decimal("125.00"))
		self.assertNotIn("ELECTRONICS15", result.applied_rules)
	
	def test_multiple_discounts(self):
		"""Test applying multiple discount rules."""
		self.engine.add_rule(self.percentage_rule)
		self.engine.add_rule(self.category_rule)
		
		result = self.engine.calculate_item_discount(self.item1)
		
		# Original: 10.00 * 2 = 20.00
		# Percentage discount (10%): 2.00
		# Category discount (15%): 3.00
		# Total discount: 5.00
		# Final: 15.00
		self.assertEqual(result.original_amount, Decimal("20.00"))
		self.assertEqual(result.discount_amount, Decimal("5.00"))
		self.assertEqual(result.final_amount, Decimal("15.00"))
		self.assertIn("PERCENT10", result.applied_rules)
		self.assertIn("ELECTRONICS15", result.applied_rules)
	
	def test_cart_discount_calculation(self):
		"""Test calculating discount for entire cart."""
		self.engine.add_rule(self.percentage_rule)
		
		cart_items = [self.item1, self.item2]
		result = self.engine.calculate_cart_discount(cart_items)
		
		# Item1: 20.00 - 2.00 = 18.00
		# Item2: 125.00 - 12.50 = 112.50
		# Total: 145.00 - 14.50 = 130.50
		self.assertEqual(result.original_amount, Decimal("145.00"))
		self.assertEqual(result.discount_amount, Decimal("14.50"))
		self.assertEqual(result.final_amount, Decimal("130.50"))
	
	def test_max_discount_limit(self):
		"""Test maximum discount limit enforcement."""
		limited_rule = DiscountRule(
			rule_id="LIMITED",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("50.00"),
			max_discount=Decimal("5.00")
		)
		
		self.engine.add_rule(limited_rule)
		result = self.engine.calculate_item_discount(self.item1)
		
		# Would be 50% of 20.00 = 10.00, but limited to 5.00
		self.assertEqual(result.discount_amount, Decimal("5.00"))
	
	def test_discount_cannot_exceed_item_total(self):
		"""Test that discount never exceeds item total."""
		huge_discount = DiscountRule(
			rule_id="HUGE",
			discount_type=DiscountType.FIXED_AMOUNT,
			value=Decimal("50.00")  # Much larger than item price
		)
		
		self.engine.add_rule(huge_discount)
		result = self.engine.calculate_item_discount(self.item1)
		
		# Discount should be capped at item total
		self.assertEqual(result.discount_amount, Decimal("20.00"))
		self.assertEqual(result.final_amount, Decimal("0.00"))


class TestValidators(unittest.TestCase):
	"""Test cases for validation functions."""
	
	def test_valid_cart_item(self):
		"""Test validation of valid cart item."""
		item = CartItem(
			item_id="VALID001",
			name="Valid Product",
			price=Decimal("15.99"),
			quantity=3,
			category="test"
		)
		
		# Should not raise any exception
		validate_cart_item(item)
	
	def test_invalid_cart_item_price(self):
		"""Test validation with invalid price."""
		item = CartItem(
			item_id="INVALID001",
			name="Invalid Product",
			price=Decimal("-5.00"),  # Negative price
			quantity=1
		)
		
		with self.assertRaises(ValidationError):
			validate_cart_item(item)
	
	def test_invalid_cart_item_quantity(self):
		"""Test validation with invalid quantity."""
		item = CartItem(
			item_id="INVALID002",
			name="Invalid Product",
			price=Decimal("10.00"),
			quantity=0  # Zero quantity
		)
		
		with self.assertRaises(ValidationError):
			validate_cart_item(item)
	
	def test_valid_discount_rule(self):
		"""Test validation of valid discount rule."""
		rule = DiscountRule(
			rule_id="VALID_RULE",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("15.00")
		)
		
		# Should not raise any exception
		validate_discount_rule(rule)
	
	def test_invalid_percentage_over_100(self):
		"""Test validation with percentage over 100%."""
		rule = DiscountRule(
			rule_id="INVALID_PERCENT",
			discount_type=DiscountType.PERCENTAGE,
			value=Decimal("150.00")  # Over 100%
		)
		
		with self.assertRaises(ValidationError):
			validate_discount_rule(rule)
	
	def test_bulk_rule_without_min_quantity(self):
		"""Test validation of bulk rule without minimum quantity."""
		rule = DiscountRule(
			rule_id="INVALID_BULK",
			discount_type=DiscountType.BULK_QUANTITY,
			value=Decimal("20.00")
			# Missing min_quantity
		)
		
		with self.assertRaises(ValidationError):
			validate_discount_rule(rule)
	
	def test_category_rule_without_category(self):
		"""Test validation of category rule without category."""
		rule = DiscountRule(
			rule_id="INVALID_CATEGORY",
			discount_type=DiscountType.CATEGORY,
			value=Decimal("10.00")
			# Missing category
		)
		
		with self.assertRaises(ValidationError):
			validate_discount_rule(rule)


if __name__ == "__main__":
	unittest.main()