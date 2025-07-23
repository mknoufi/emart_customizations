# Copyright (c) 2025, nou and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Salesman"),
			"fieldname": "salesman",
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 150
		},
		{
			"label": _("Target Amount"),
			"fieldname": "target_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Achieved Amount"),
			"fieldname": "achieved_amount", 
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Achievement %"),
			"fieldname": "achievement_percentage",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Variance"),
			"fieldname": "variance",
			"fieldtype": "Currency",
			"width": 120
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql(f"""
		SELECT 
			st.salesman,
			st.target_amount,
			st.achieved_amount,
			st.achievement_percentage,
			(st.achieved_amount - st.target_amount) as variance
		FROM `tabSalesman Target` st
		WHERE st.docstatus = 1 {conditions}
		ORDER BY st.achievement_percentage DESC
	""", filters, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"):
		conditions += " AND st.from_date >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND st.to_date <= %(to_date)s"
		
	if filters.get("salesman"):
		conditions += " AND st.salesman = %(salesman)s"
	
	return conditions