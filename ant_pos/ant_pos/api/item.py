import frappe
import json
from frappe import _ 
from erpnext.stock.get_item_details import get_item_details , get_item_price , apply_price_list
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
BarcodeScanResult = dict[str, str | None]


def _update_item_info(scan_result: dict[str, str | None]) -> dict[str, str | None]:
	if item_code := scan_result.get("item_code"):
		if item_info := frappe.get_cached_value(
			"Item",
			item_code,
			["has_batch_no", "has_serial_no"],
			as_dict=True,
		):
			scan_result.update(item_info)
	return scan_result

@frappe.whitelist()
def scan_barcode(search_value: str) -> BarcodeScanResult:
      
	def set_cache(data: BarcodeScanResult):
		frappe.cache().set_value(f"ant_pos:barcode_scan:{search_value}", data, expires_in_sec=120)
            
	def get_cache() -> BarcodeScanResult | None:
		if data := frappe.cache().get_value(f"ant_pos:barcode_scan:{search_value}"):
			return data
	if scan_data := get_cache():
		return scan_data
	# search barcode no
	barcode_data = frappe.db.get_value(
		"Item Barcode",
		{"barcode": search_value},
		["barcode", "parent as item_code", "uom"],
		as_dict=True,
	)
	if barcode_data:
		barcode_data.item = frappe.db.get_value('Item',barcode_data.item_code , ['*'], as_dict=1)
		_update_item_info(barcode_data)
		set_cache(barcode_data)
		return barcode_data
	# search serial no
	serial_no_data = frappe.db.get_value(
		"Serial No",
		search_value,
		["name as serial_no", "item_code", "batch_no"],
		as_dict=True,
	)
	if serial_no_data:
		serial_no_data.item = frappe.db.get_value('Item',serial_no_data.item_code , ['*'], as_dict=1)
		_update_item_info(serial_no_data)
		set_cache(serial_no_data)
		return serial_no_data
	# search batch no
	batch_no_data = frappe.db.get_value(
		"Batch",
		search_value,
		["name as batch_no", "item as item_code"],
		as_dict=True,
	)
	if batch_no_data:
		batch_no_data.item = frappe.db.get_value('Item',batch_no_data.item_code , ['*'], as_dict=1)
		_update_item_info(batch_no_data)
		set_cache(batch_no_data)
		return batch_no_data
	item_code = frappe.db.get_value(
		"Item",
		search_value,
		["name as item_code"],
		as_dict=True,
	)
	if item_code:
		item_code.item = frappe.db.get_value('Item',item_code.item_code , ['*'], as_dict=1)
		_update_item_info(item_code)
		set_cache(item_code)
		return item_code
	return {}



@frappe.whitelist()
def items(pos_profile, search_value, customer):
    if not customer:
        frappe.throw(_("Please select the customer"))

    value = scan_barcode(search_value)
    if not value or not value.get("item"):
        frappe.throw(_("No item found for the given barcode."))

    pos_profile_data = frappe._dict(json.loads(pos_profile))
    company = frappe.db.get_value('Company', pos_profile_data.get('company'), ['default_currency', 'name'], as_dict=True)
    customer_doc = frappe.db.get_value('Customer', customer, ['is_internal_customer'], as_dict=True)
    item = value["item"]

    serial_nos = []
    batch_nos = []

    if item.get("has_serial_no"):
        serial_filters = {"item_code": item["item_code"], "warehouse": pos_profile_data.get('warehouse')}
        serial_nos = frappe.get_all("Serial No", filters=serial_filters, fields=["name as serial_no", "batch_no"])

    if item.get("has_batch_no"):
        batch_nos = frappe.get_all("Batch", filters={"item": item["item_code"]}, fields=["name as batch_no", "expiry_date"])

    # rate = 150
    items = {
        "item_code": item["item_code"],
        "barcode": value.get("barcode"),
        "customer": customer,
        "currency": company.get('default_currency'),
        "is_internal_customer": customer_doc.get('is_internal_customer'),
        "price_list": "Standard Selling",
        "price_list_currency": company.get('default_currency'),
        "company": company.get('name'),
        "ignore_pricing_rule": 0,
        "doctype": "Sales Invoice",
        "stock_uom": item.get('stock_uom'),
        "pos_profile": pos_profile_data.get('name'),
        "cost_center": pos_profile_data.get('cost_center'),
        "tax_category": pos_profile_data.get('tax_category'),
        "serial_no": serial_nos,
        # "rate": rate,
        "batch_no": value.get("batch_no"),
        "warehouse": pos_profile_data.get('warehouse'),
		"is_pos":1
    }

    # Fetch item details
    values = get_item_details(items, doc=None, overwrite_warehouse=False)
    # values["rate"] = rate
    values["serial_no"] = serial_nos
    values["batch_nos"] = batch_nos
    values["selected_serial_no"] = [value.get("serial_no")] if value.get("has_serial_no") and value.get("serial_no") else []
    values["selected_batch_no"]= item.get("batch_no") if value.get("has_batch_no") and item.get("batch_no") else None

    return values
