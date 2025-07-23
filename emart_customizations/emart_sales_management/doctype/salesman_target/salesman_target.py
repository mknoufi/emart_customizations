# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class SalesmanTarget(Document):
	def validate(self):
		self.calculate_achievement()
	
	def calculate_achievement(self):
		"""Calculate achievement based on actual sales"""
		if self.salesman and self.from_date and self.to_date:
			# Get sales invoices for this salesman in the period
			sales_invoices = frappe.get_all("Sales Invoice", 
				filters={
					"sales_person": self.salesman,
					"posting_date": ["between", [self.from_date, self.to_date]],
					"docstatus": 1
				},
				fields=["grand_total"]
			)
			
			self.achieved_amount = sum([flt(si.grand_total) for si in sales_invoices])
			
			if self.target_amount:
				self.achievement_percentage = (self.achieved_amount / self.target_amount) * 100