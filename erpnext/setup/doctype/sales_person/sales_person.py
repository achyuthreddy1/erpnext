# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import flt
from frappe.utils.nestedset import DocTypeNestedSet

class SalesPerson(DocTypeNestedSet):
	nsm_parent_field = 'parent_sales_person';

	def validate(self): 
		for d in self.get('target_details'):
			if not flt(d.target_qty) and not flt(d.target_amount):
				frappe.throw(_("Either target qty or target amount is mandatory."))
	
	def on_update(self):
		super(SalesPerson, self).on_update()
		self.validate_one_root()
	
	def get_email_id(self):
		if self.employee:
			user = frappe.db.get_value("Employee", self.employee, "user_id")
			if not user:
				frappe.throw("User ID not set for Employee %s" % self.employee)
			else:
				return frappe.db.get_value("User", user, "email") or user