# Event handlers for sales management

import frappe
from frappe.utils import flt


def update_salesman_achievement(doc, method):
	"""Update salesman achievement when sales invoice is submitted"""
	if doc.sales_person:
		# Find active targets for this salesman
		targets = frappe.get_all("Salesman Target",
			filters={
				"salesman": doc.sales_person,
				"from_date": ["<=", doc.posting_date],
				"to_date": [">=", doc.posting_date],
				"docstatus": 1
			}
		)
		
		for target in targets:
			target_doc = frappe.get_doc("Salesman Target", target.name)
			target_doc.calculate_achievement()
			target_doc.save()