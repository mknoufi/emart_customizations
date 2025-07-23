# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseIncentive(Document):
	def validate(self):
		self.calculate_incentive_amount()
	
	def calculate_incentive_amount(self):
		"""Calculate incentive amount based on type and percentage"""
		if self.incentive_type == "Percentage" and self.incentive_percentage:
			if self.purchase_order:
				po = frappe.get_doc("Purchase Order", self.purchase_order)
				self.total_purchase_amount = po.grand_total
				self.incentive_amount = (self.total_purchase_amount * self.incentive_percentage) / 100
			elif self.total_purchase_amount:
				self.incentive_amount = (self.total_purchase_amount * self.incentive_percentage) / 100
		elif self.incentive_type == "Fixed Amount":
			# Incentive amount is manually set
			pass