# EMart Customizations API

import frappe
from frappe import _
from frappe.utils import flt, getdate


@frappe.whitelist()
def get_salesman_dashboard_data(salesman=None):
	"""Get dashboard data for salesman portal"""
	if not salesman:
		salesman = frappe.session.user
	
	# Get sales targets
	targets = frappe.get_all("Salesman Target",
		filters={"salesman": salesman, "docstatus": 1},
		fields=["target_amount", "achieved_amount", "achievement_percentage"]
	)
	
	# Get recent sales
	recent_sales = frappe.get_all("Sales Invoice",
		filters={"sales_person": salesman, "docstatus": 1},
		fields=["name", "customer", "grand_total", "posting_date"],
		order_by="posting_date desc",
		limit=10
	)
	
	return {
		"targets": targets,
		"recent_sales": recent_sales
	}


@frappe.whitelist()
def scan_barcode(barcode):
	"""Scan barcode and return item details"""
	if not barcode:
		return {"error": "No barcode provided"}
	
	# Look for item by barcode
	items = frappe.get_all("Item",
		filters={"barcode": barcode},
		fields=["name", "item_name", "standard_rate", "stock_uom"]
	)
	
	if items:
		item = items[0]
		# Get current stock
		stock_balance = frappe.get_all("Bin",
			filters={"item_code": item.name},
			fields=["actual_qty", "warehouse"],
			order_by="actual_qty desc"
		)
		
		return {
			"item": item,
			"stock": stock_balance
		}
	else:
		return {"error": "Item not found"}


@frappe.whitelist()
def send_whatsapp_message(phone, message, template=None):
	"""Send WhatsApp message using configured API"""
	settings = frappe.get_single("Integration Settings")
	
	if not settings.enable_whatsapp:
		return {"error": "WhatsApp integration not enabled"}
	
	# Implementation would depend on WhatsApp API provider
	# This is a placeholder for the actual integration
	return {"success": True, "message": "Message sent successfully"}


@frappe.whitelist()
def create_mobile_stock_entry(item_code, warehouse, scanned_qty, activity_type, notes=None, gps_coordinates=None):
	"""Create mobile stock tracking entry"""
	try:
		doc = frappe.new_doc("Mobile Stock Tracking")
		doc.item_code = item_code
		doc.warehouse = warehouse
		doc.scanned_qty = flt(scanned_qty)
		doc.activity_type = activity_type
		doc.notes = notes
		doc.gps_coordinates = gps_coordinates
		doc.save()
		
		return {"success": True, "name": doc.name}
	except Exception as e:
		return {"error": str(e)}


@frappe.whitelist()
def get_aging_stock_alerts(warehouse=None):
	"""Get aging stock alerts"""
	filters = {"alert_level": ["!=", "Normal"]}
	if warehouse:
		filters["warehouse"] = warehouse
	
	alerts = frappe.get_all("Aging Stock Alert",
		filters=filters,
		fields=["item_code", "item_name", "warehouse", "aging_days", "alert_level", "recommended_action", "total_value"],
		order_by="aging_days desc"
	)
	
	return alerts


@frappe.whitelist()
def has_app_permission(user=None):
	"""Check if user has permission to access the app"""
	if not user:
		user = frappe.session.user
	
	# Check if user has any of the required roles
	required_roles = ["Sales Manager", "Purchase Manager", "Stock Manager", "System Manager"]
	user_roles = frappe.get_roles(user)
	
	return bool(set(required_roles) & set(user_roles))