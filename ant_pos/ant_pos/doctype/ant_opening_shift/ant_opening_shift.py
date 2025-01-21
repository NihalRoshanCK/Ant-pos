# Copyright (c) 2024, Nihal Roshan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from  ant_pos.ant_pos.utils.employee import is_employee

class AntOpeningShift(Document):
	def validate (self):
		if not self.set_posting_date:
			self.period_start_date=frappe.utils.today()
		if self.posting_date:
			if frappe.utils.date_diff(self.period_start_date , self.period_end_date) > 0 :
				frappe.throw("Posting Date is  cannot be grater than  Period Start Date ")
		if not self.cashier:
			self.cashier=frappe.session.user
		self.posting_date=frappe.utils.today()
		if self.get_openingshift_for_user(self.cashier):
			frappe.throw("casher already as a open shift")
		# if not is_employee(self.cashier):
		# 	frappe.throw("the casher need to be an employee")
		
	def get_openingshift_for_user(self,user):
		return frappe.db.exists("Ant Opening Shift", {"cashier": user,'docstatus':1,'status': 'Open'})