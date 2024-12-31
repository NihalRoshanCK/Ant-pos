import frappe
from frappe import _
from ant_pos.ant_pos.doctype.ant_opening_shift.ant_opening_shift import AntOpeningShift

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


@frappe.whitelist()
def create_opening(values):
    """
    Creates a new Ant Opening Shift document with the given values.

    Args:
        values (dict): A dictionary containing the field names and their respective values.

    Returns:
        str: The name of the newly created Ant Opening Shift document.
    """
    try:
        # Validate input
        if not isinstance(values, dict):
            frappe.throw("Invalid data format. Expected a dictionary.")

        # Create a new Ant Opening Shift document
        ant_opening_shift = frappe.new_doc("Ant Opening Shift")
        
        # Set field values from the `values` dictionary
        for field, value in values.items():
            ant_opening_shift.set(field, value)

        # Insert the document into the database
        ant_opening_shift.insert()

        ant_opening_shift.submit()

        # Optionally, submit the document if it requires workflow completion
        # ant_opening_shift.submit()

        # Return the name of the new document
        return ant_opening_shift.name

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Ant Opening Shift Creation Error")
        frappe.throw(str(e))






# @frappe.whitelist()
# def get_items(pos_profile, search_value, price_list='Standard Selling'):
#     print(search_value, "search_value")
#     print(pos_profile, "theeeeeeeeeeeeeeeeeeeeeeeeeeeeeee po profilee")
#     # Cache to store the results of frequent queries
#     cache = {}

#     # Helper function to fetch and cache data
#     def fetch_data(doctype, filters, fields):
#         print("134**************************************")
#         print(doctype, filters, fields)
#         cache_key = (doctype, frozenset(filters.items()))
#         if cache_key not in cache:
#             cache[cache_key] = frappe.db.get_value(
#                 doctype, filters, fields, as_dict=True
#             )

#         print(cache.get(cache_key), "cache.get(cache_key)cache.get(cache_key)")
#         return cache.get(cache_key)

#     # Extract warehouse from pos_profile
#     warehouse = pos_profile.get("warehouse")
#     print(warehouse,"147******************************")

#     # Check if the search_value is a barcode
#     barcode_data = fetch_data(
#         "Item Barcode", {"barcode": search_value}, ["barcode", "parent as item_code", "uom"]
#     )
#     if barcode_data:
#         return update_items("Item Barcode", barcode_data, price_list, warehouse)

#     # Check if the search_value is a serial number
#     serial_no_data = fetch_data(
#         "Serial No", {"name": search_value, "warehouse": warehouse}, ["name as serial_no", "item_code", "batch_no"]
#     )
#     print(serial_no_data, "serial_no_data")
#     if serial_no_data:
#         return update_items("Serial No", serial_no_data, price_list, warehouse)

#     # Check if the search_value is a batch number
#     batch_no_data = fetch_data(
#         "Batch", {"name": search_value}, ["*"]
#     )
#     print(batch_no_data, "batch_no_data")
#     if batch_no_data:
#         return update_items("Batch", batch_no_data, price_list, warehouse)

#     # Check if the search_value is an item code or name
#     item_data = fetch_data(
#         "Item", {"name": search_value}, [
#             "item_code", "item_name", "description", "item_group", "stock_uom",
#             "has_serial_no", "has_batch_no"
#         ]
#     )
#     if item_data:
#         return update_items("Item", item_data, price_list, warehouse)

#     # If no match found, return None
#     return None

# def update_items(doctype, scan_result, price_list, warehouse):
#     # Fetch detailed data based on the document type
#     fields_to_fetch = ['*']

#     # Fetch additional details for the item
#     if doctype == "Item":
#         item_details = frappe.db.get_value(
#             "Item", scan_result.get("item_code"), fields_to_fetch, as_dict=True
#         )
#         rate = get_item_rate(scan_result.get("item_code"), price_list, warehouse)
#         return {**scan_result, **item_details, "rate": rate}
    
#     elif doctype == "Serial No":
#         item_details = frappe.db.get_value(
#             "Item", scan_result.get("item_code"), fields_to_fetch, as_dict=True
#         )
#         rate = get_item_rate(scan_result.get("item_code"), price_list)
#         return {**scan_result, **item_details, "rate": rate}

#     # Add more conditions here if needed for other doctype like Batch, Item Barcode etc.

#        # Handle the Batch doctype and fetch serial numbers
#     elif doctype == "Batch":
#         item_code = scan_result.get("item_code")
#         serial_numbers = frappe.db.get_list(
#             "Serial No",
#             filters={
#                 "batch_no": scan_result.get("name"),
#                 "warehouse": warehouse
#             },
#             fields=["name"]
#         )
#         serial_number_list = [sn["name"] for sn in serial_numbers]
        
#         # Include batch details and serial number list
#         return {
#             **scan_result,
#             "serial_numbers": serial_number_list,
#             "serial_number_count": len(serial_number_list)
#         }

#     # Add more conditions here if needed for other doctypes like Item Barcode etc.

#     return scan_result


# def get_item_rate(item_code, price_list):
#     rate = frappe.db.get_value(
#         "Item Price",
#         {"item_code": item_code, "price_list": price_list},
#         "price_list_rate"
#     )
#     return rate if rate else 0




