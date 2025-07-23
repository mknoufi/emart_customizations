# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IntegrationSettings(Document):
	def validate(self):
		if self.enable_whatsapp and not self.whatsapp_api_key:
			frappe.throw("WhatsApp API Key is required when WhatsApp integration is enabled")
		
		if self.enable_tally_sync and not self.tally_server_ip:
			frappe.throw("Tally Server IP is required when Tally sync is enabled")
		
		if self.enable_biometric and not self.biometric_device_ip:
			frappe.throw("Biometric Device IP is required when biometric integration is enabled")