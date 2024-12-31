import frappe
import json
from frappe import _ 
# from erpnext.accounts.doctype.pricing_rule.pricing_rule import  apply_pricing_rule,get_pricing_rule_for_item
from erpnext.stock.get_item_details import get_item_details
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


# @frappe.whitelist()
# def items(pos_profile,search_value,customer ):
#     """
#     Fetch item details, including serial numbers if applicable.
#     """
#     value = scan_barcode(search_value)
#     if not value or not value.item:
#         frappe.throw(("No item found for the given barcode."))
# 	item = value.item
# 		if item:

	# if item.has_serial_no:
	# 	serial_nos = frappe.get_all(
	# 	"Serial No",
	# 	filters={"item_code": item.item_code, "warehouse": pos_profile.warehouse},
	# 	fields=["name as serial_no", "batch_no"],
	# 	)
	# 	value["serial_nos"] = serial_nos
	# if item.has_batch_no:
	# 	batch_nos = frappe.get_all(
	# 		"Batch",
	# 	filters={"item": item.item_code},
	# 	fields=["name as batch_no", "expiry_date"],
	# 	)
	# 	value["batch_nos"] = batch_nos
# from frappe.utils import cstr, comma_and, cint
# frappe.throw(
# 				_("Rows {0} have the duplicate questions.").format(frappe.bold(comma_and(rows)))
# 			)

    
@frappe.whitelist()
def items(pos_profile, search_value, customer):
	if not customer:
		frappe.throw(
					_("please select the customer ")
					)
	print(customer, "customer$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	# frappe.throw(
	# 			_("please select the customer ").format(frappe.bold(""))
	# 			)
	value = scan_barcode(search_value)
	pos_profile_data = frappe._dict(json.loads(pos_profile))
	# pos_profile_data = frappe.get_doc('POS Profile', pos_profile) if pos_profile else None
	print(pos_profile_data, "pos_profile@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	company = frappe.db.get_value('Company',pos_profile_data.get('company'), ['*'], as_dict=1)
	customer_doc = frappe.db.get_value('Customer',customer, ['*'], as_dict=1)
	uom_conversion = frappe.db.get_value('UOM Conversion Detail', value.item.uoms, ['*'], as_dict=1)
	item_price = frappe.db.get_value('Item Price', {'item_code': value.item.item_code, 'price_list': 'Standard Selling',"batch_no":value.batch_no}, ['*'], as_dict=1)
	print(item_price, "item_price************************************")
	item = value.item
	if item:
		items={
    		"item_code":item.item_code,
    		"barcode":value.barcode,
    		"customer":customer,
    		"currency":company.get('default_currency'),
    		"is_internal_customer":customer_doc.get('is_internal_customer'),
			"price_list":"Standard Selling",
			"price_list_currency":company.get('default_currency'),
			"company":company.get('name'),
			"ignore_pricing_rule":0,
			"doctype":"Sales Invoice",
			"stock_uom":item.get('stock_uom'),
			"pos_profile":pos_profile_data.get('name'),
			"cost_center":pos_profile_data.get('cost_center'),
			"tax_category":pos_profile_data.get('tax_category'),
		}
		rule = get_item_details(items, doc=None,overwrite_warehouse=False,)
		return rule


