# Scheduled tasks for integrations

import frappe
import requests
from frappe.utils import now


def sync_tally_data():
	"""Sync data with Tally ERP"""
	settings = frappe.get_single("Integration Settings")
	
	if not settings.enable_tally_sync:
		return
	
	try:
		# Placeholder for Tally integration logic
		# This would involve XML requests to Tally's HTTP API
		
		# Update last sync time
		settings.last_sync = now()
		settings.save()
		
		frappe.logger().info("Tally sync completed successfully")
		
	except Exception as e:
		frappe.logger().error(f"Tally sync failed: {str(e)}")


def sync_biometric_data():
	"""Sync attendance data from biometric devices"""
	settings = frappe.get_single("Integration Settings")
	
	if not settings.enable_biometric:
		return
	
	try:
		# Placeholder for biometric device integration
		# This would connect to the biometric device API
		
		frappe.logger().info("Biometric sync completed successfully")
		
	except Exception as e:
		frappe.logger().error(f"Biometric sync failed: {str(e)}")