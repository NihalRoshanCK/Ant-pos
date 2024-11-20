import frappe
from frappe import _


@frappe.whitelist()
def get_openingshift():
    user=frappe.session.user
    open_vouchers = frappe.db.get_all(
        "Ant Opening Shift",
        filters={
            "cashier": user,
            "ant_closing_shift_detail": ["in", ["", None]],
            "docstatus": 1,
            "status": "Open",
        },
        fields=["name", "pos_profile"],
        order_by="period_start_date desc"
    )
    data = ""
    if len(open_vouchers) > 0:
        data = {}
        data["Ant_Opening_Shift"] = frappe.get_doc(
            "Ant Opening Shift", open_vouchers[0]["name"]
        )
        data['pos_profile']=get_pos_profile(data["Ant_Opening_Shift"].pos_profile)
        # update_opening_shift_data(data, open_vouchers[0]["pos_profile"])
    return data

@frappe.whitelist()
def get_pos_profile(profile):
    pos=frappe.get_doc("POS Profile", profile)
    return pos