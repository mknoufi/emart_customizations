# Event handlers for purchase management

import frappe


def calculate_purchase_incentive(doc, method):
	"""Calculate purchase incentive when purchase order is submitted"""
	if doc.supplier:
		# Find active incentives for this supplier
		incentives = frappe.get_all("Purchase Incentive",
			filters={
				"supplier": doc.supplier,
				"status": "Active"
			}
		)
		
		for incentive in incentives:
			incentive_doc = frappe.get_doc("Purchase Incentive", incentive.name)
			incentive_doc.total_purchase_amount = doc.grand_total
			incentive_doc.calculate_incentive_amount()
			incentive_doc.save()