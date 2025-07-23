# Event handlers for inventory management

import frappe
from frappe.utils import getdate, date_diff


def check_aging_stock(doc, method):
	"""Check for aging stock when stock ledger entry is created"""
	if doc.actual_qty > 0:  # Only for incoming stock
		# Check if aging alert already exists
		existing_alert = frappe.get_all("Aging Stock Alert",
			filters={
				"item_code": doc.item_code,
				"warehouse": doc.warehouse
			}
		)
		
		if not existing_alert:
			# Create new aging stock alert
			aging_alert = frappe.new_doc("Aging Stock Alert")
			aging_alert.item_code = doc.item_code
			aging_alert.warehouse = doc.warehouse
			aging_alert.save()