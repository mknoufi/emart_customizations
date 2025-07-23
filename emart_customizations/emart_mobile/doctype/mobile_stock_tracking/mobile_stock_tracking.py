# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class MobileStockTracking(Document):
	def before_save(self):
		self.update_system_qty()
		self.calculate_variance()
	
	def update_system_qty(self):
		"""Get current system quantity for comparison"""
		if self.item_code and self.warehouse:
			bin_data = frappe.get_all("Bin",
				filters={
					"item_code": self.item_code,
					"warehouse": self.warehouse
				},
				fields=["actual_qty"]
			)
			
			if bin_data:
				self.system_qty = bin_data[0].actual_qty
			else:
				self.system_qty = 0
	
	def calculate_variance(self):
		"""Calculate variance between scanned and system quantity"""
		if self.scanned_qty is not None and self.system_qty is not None:
			self.variance = self.scanned_qty - self.system_qty
	
	def before_insert(self):
		if not self.timestamp:
			self.timestamp = now()
		if not self.user:
			self.user = frappe.session.user