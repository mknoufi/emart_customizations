# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class DamageTracking(Document):
	def before_save(self):
		self.update_item_details()
		self.calculate_estimated_loss()
	
	def update_item_details(self):
		"""Update item details from Item master"""
		if self.item_code:
			item = frappe.get_doc("Item", self.item_code)
			self.item_name = item.item_name
	
	def calculate_estimated_loss(self):
		"""Calculate estimated loss based on item valuation"""
		if self.item_code and self.warehouse and self.damaged_qty:
			# Get current valuation rate
			valuation_rate = frappe.db.get_value("Bin", 
				{"item_code": self.item_code, "warehouse": self.warehouse}, 
				"valuation_rate")
			
			if valuation_rate:
				self.estimated_loss = flt(self.damaged_qty) * flt(valuation_rate)
	
	def before_insert(self):
		if not self.reported_by:
			self.reported_by = frappe.session.user
	
	def on_submit(self):
		"""Create stock entry for write-off if required"""
		if self.write_off_required and self.approval_status == "Approved":
			self.create_stock_entry_for_writeoff()
	
	def create_stock_entry_for_writeoff(self):
		"""Create stock entry to write off damaged stock"""
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Issue"
		stock_entry.purpose = "Material Issue"
		
		stock_entry.append("items", {
			"item_code": self.item_code,
			"qty": self.damaged_qty,
			"s_warehouse": self.warehouse,
			"cost_center": frappe.defaults.get_user_default("Cost Center") or frappe.db.get_single_value("Company", "cost_center")
		})
		
		stock_entry.insert()
		stock_entry.submit()
		
		# Link the stock entry to this damage tracking record
		self.db_set("stock_entry", stock_entry.name)