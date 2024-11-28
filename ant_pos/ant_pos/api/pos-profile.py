import frappe
from frappe import _


@frappe.whitelist()
def get_openingshift():
    user = frappe.session.user
    open_vouchers = frappe.db.get_all(
        "Ant Opening Shift",
        filters={
            "cashier": user,
            "ant_closing_shift_detail": ["in", ["", None]],
            "docstatus": 1,
            "status": "Open",
        },
        fields=["name", "pos_profile"],
        order_by="period_start_date desc",
    )
    data = ""
    if open_vouchers:
        data = {}
        data["Ant_Opening_Shift"] = frappe.get_doc(
            "Ant Opening Shift", open_vouchers[0]["name"]
        )
        data["pos_profile"] = get_pos_profile(data["Ant_Opening_Shift"].pos_profile)
    return data


@frappe.whitelist()
def get_pos_profile(profile):
    pos = frappe.get_doc("POS Profile", profile)
    return pos


@frappe.whitelist()
def get_pos_profiles_by_company():
    # Fetch all POS Profiles with associated company
    pos_profiles = frappe.get_all(
        "POS Profile",
        fields=["name", "company"],
        order_by="company ASC",
    )
    company_profiles = {}

    for profile in pos_profiles:
        company = profile["company"]
        pos_name = profile["name"]

        if company not in company_profiles:
            company_profiles[company] = []

        # Fetch modes of payment for the current POS Profile
        modes_of_payment = frappe.get_all(
            "POS Payment Method",
            filters={"parent": pos_name},  # Assuming "parent" links to POS Profile
            fields=["mode_of_payment"],
        )

        # Append POS Profile with its modes of payment
        company_profiles[company].append({
            "name": pos_name,
            "modes_of_payment": [mop["mode_of_payment"] for mop in modes_of_payment],
        })

    # Optional: Log for debugging during development
    print("Company Profiles Data with Modes of Payment:", company_profiles)

    return company_profiles
