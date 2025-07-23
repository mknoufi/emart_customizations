# Scheduled tasks for inventory management

import frappe
from frappe.utils import getdate, date_diff


def generate_aging_stock_alerts():
	"""Generate aging stock alerts for items older than configured threshold"""
	
	# Get all unique item-warehouse combinations
	stock_entries = frappe.db.sql("""
		SELECT DISTINCT sle.item_code, sle.warehouse, MIN(sle.posting_date) as first_entry
		FROM `tabStock Ledger Entry` sle
		INNER JOIN `tabBin` bin ON bin.item_code = sle.item_code AND bin.warehouse = sle.warehouse
		WHERE bin.actual_qty > 0
		GROUP BY sle.item_code, sle.warehouse
	""", as_dict=True)
	
	for entry in stock_entries:
		aging_days = date_diff(getdate(), entry.first_entry)
		
		if aging_days >= 60:  # Alert for items older than 60 days
			# Check if alert already exists
			existing_alert = frappe.get_all("Aging Stock Alert",
				filters={
					"item_code": entry.item_code,
					"warehouse": entry.warehouse
				}
			)
			
			if not existing_alert:
				# Create new aging stock alert
				aging_alert = frappe.new_doc("Aging Stock Alert")
				aging_alert.item_code = entry.item_code
				aging_alert.warehouse = entry.warehouse
				aging_alert.save()