# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff


class AgingStockAlert(Document):
	def before_save(self):
		self.update_item_details()
		self.calculate_aging()
		self.set_alert_level()
	
	def update_item_details(self):
		"""Update item details from Item master"""
		if self.item_code:
			item = frappe.get_doc("Item", self.item_code)
			self.item_name = item.item_name
	
	def calculate_aging(self):
		"""Calculate aging days based on stock ledger entries"""
		if self.item_code and self.warehouse:
			# Get the oldest stock entry
			stock_entries = frappe.get_all("Stock Ledger Entry",
				filters={
					"item_code": self.item_code,
					"warehouse": self.warehouse,
					"actual_qty": [">", 0]
				},
				fields=["posting_date"],
				order_by="posting_date asc",
				limit=1
			)
			
			if stock_entries:
				oldest_date = stock_entries[0].posting_date
				self.aging_days = date_diff(getdate(), oldest_date)
			
			# Get current stock and valuation
			stock_balance = frappe.get_all("Bin",
				filters={
					"item_code": self.item_code,
					"warehouse": self.warehouse
				},
				fields=["actual_qty", "valuation_rate"]
			)
			
			if stock_balance:
				self.current_stock = stock_balance[0].actual_qty
				self.valuation_rate = stock_balance[0].valuation_rate
				self.total_value = self.current_stock * self.valuation_rate
	
	def set_alert_level(self):
		"""Set alert level based on aging days"""
		if self.aging_days >= 180:
			self.alert_level = "Critical"
			self.recommended_action = "Clearance Sale"
		elif self.aging_days >= 90:
			self.alert_level = "Warning"  
			self.recommended_action = "Discount Sale"
		else:
			self.alert_level = "Normal"
			self.recommended_action = "No Action"