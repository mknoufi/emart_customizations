"""Product Discount Calculator Module

This module provides comprehensive discount calculation functionality
for e-commerce and POS systems.
"""

from .discount_engine import DiscountEngine, DiscountRule, DiscountType, CartItem, DiscountResult
from .validators import validate_cart_item, validate_discount_rule, ValidationError

__all__ = [
	"DiscountEngine",
	"DiscountRule", 
	"DiscountType",
	"CartItem",
	"DiscountResult",
	"validate_cart_item",
	"validate_discount_rule",
	"ValidationError",
]