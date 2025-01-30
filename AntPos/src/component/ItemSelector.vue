<template>
    <div class="w-1/2 shadow-2xl pt-2 px-2  rounded">
        <div>
            <div>
                <FormControl
                    type="text"
                    v-model="debounceSearch"
                    placeholder="Search Items"
                    size="sm"
                    variant="subtle"
                    @keyup.enter="searchResource.fetch()"
                >
                    <template #prefix>
                        <FeatherIcon class="w-4" name="search" />
                    </template>
                </FormControl>
                <div>
                    <div v-if="items.length === 0" class="text-center text-gray-500">
                        No items found. Try searching again.
                    </div>
                    <div v-else>
                        <div class="flex justify-between items-center border-b pb-4">
                            <div class="flex justify-between w-full">
                                <span class="text-lg font-medium mr-4">{{ items.item_code }}</span>
                                <span class="text-sm text-gray-500">Qty: 1</span>
                                <span class="text-sm text-gray-500">Price: {{ items.rate }}</span>
                                <span class="text-lg font-semibold ml-4">{{ items.serial_no }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { FormControl, FeatherIcon, createResource } from 'frappe-ui';
import { ref, inject } from 'vue';

// Reactive variables
const debounceSearch = ref('');
const items = ref([]);
let base = inject('base');

// Search resource with debounce
const searchResource = createResource({
    url: 'ant_pos.ant_pos.api.item.scan_barcode',
    method: 'GET',
    debounce: 300,
    makeParams() {
        return {
            search_value: debounceSearch.value,
        };
    },
    validate(params) {
        if (!params.search_value) {
            return 'Search value is required';
        }
        if (!base.customer) {
            return 'Please select a customer';
        }
    },
    onSuccess(data) {
        if (data.serial_no) {
            data.selected_serial_no = [data.serial_no];
        }
        if (!addItemIfExists(data)) {
            addItemsResource.fetch({ search_value: JSON.stringify(data) });
        }
    },
    onError(error) {
        console.error('Search error:', error);
    },
});

// Add items resource
const addItemsResource = createResource({
    url: 'ant_pos.ant_pos.api.item.items',
    method: 'GET',
    debounce: 500,
    initialData: [],
    makeParams(params) {
        return {
            pos_profile: JSON.stringify(base.pos_profile),
            search_value: params.search_value,
            customer: base.customer.name,
        };
    },
    validate(params) {
        if (!params.search_value) {
            return 'Search value is required';
        }
    },
    onError(error) {
        console.error('Add items error:', error);
    },
    onSuccess(data) {
        addItem(data);
    },
});
const priceRuleRemover = createResource({
    url: 'erpnext.accounts.doctype.pricing_rule.pricing_rule.remove_pricing_rule_for_item', 
    method: 'POST', 
    auto: false,
    makeParams() {
        return {
            pricing_rules: [
                "PRLE-0003"
                ],  
            item_details: {"doctype":"Sales Invoice Item","name":"new-sales-invoice-item-otqwuoxyib","item_code":"SR-MWR-SRT-LINEN-HS","pricing_rules":"[\n \"PRLE-0003\"\n]","parenttype":"Sales Invoice","parent":"new-sales-invoice-qvfaljieei","price_list_rate":0},
            item_code: SR-MWR-SRT-LINEN-HS,
            rate: 0

        };
    },
    onError(error) {
    },
    onSuccess(data) {
    }
});
const priceListResource = createResource({
    url: 'erpnext.stock.get_item_details.apply_price_list', 
    method: 'POST', 
    makeParams(params) {
        return {
            args: JSON.stringify({
                items: [
                    {
                    "doctype": "Sales Invoice Item",
                    "name": "new-sales-invoice-item-lrdmbgmbcz",
                    "child_docname": "new-sales-invoice-item-lrdmbgmbcz",
                    "item_code": params.items.item_code,
                    "item_group":params.items.item_group,
                    "brand": params.items.brand,
                    "qty": params.items.qty,
                    "stock_qty": params.items.stock_qty,
                    "uom": params.items.uom,
                    "stock_uom": params.items.stock_uom,
                    "parenttype": "Sales Invoice",
                    "parent": "new-sales-invoice-owspmikswv",
                    "pricing_rules": params.items.pricing_rules,
                    "is_free_item": params.items.is_free_item,
                    "warehouse": params.items.warehouse,
                    "serial_no": base.items.selected_serial_no,
                    "batch_no": params.items.batch_no,
                    "price_list_rate": params.items.price_list_rate,
                    "conversion_factor": params.items.conversion_factor,
                    "margin_type": params.items.margin_type,
                    "margin_rate_or_amount": params.items.margin_rate_or_amount,
                    }
                ],
                    "customer":base.customer.name,
                    "customer_group":  base.customer.customer_group,
                    "territory": base.customer.territory,
                    "currency":base.pos_profile.currency,
                    "conversion_rate": 1,
                    "price_list": "Standard Selling",
                    "price_list_currency": base.pos_profile.currency,
                    "plc_conversion_rate": 1,
                    "company": base.pos_profile.company,
                    "transaction_date": "",
                    "ignore_pricing_rule": 0,
                    "doctype": "Sales Invoice",
                    "name": "new-sales-invoice-owspmikswv",
                    "is_return": 0,
                    "update_stock": 1,
                    "pos_profile": base.pos_profile.name,
                    "is_internal_customer": base.customer.is_internal_customer,
            })
        };
    },
    onError(error) {
        console.error('Price list error:', error);
    },
    onSuccess(data) {
        return data;

    }
});


// Add item to the list
const addItem = (data) => {
    data.doctype="Sales Invoice Item";
    data.parenttype="Sales Invoice"
    if (!addItemIfExists(data)) {
        if (data.has_batch_no && data.batch_no) {
            data.serial_no_options = data.serial_no
                .filter(serial_no => data.batch_no && serial_no.batch_no === data.batch_no)
                .map(serial_no => ({
                    label: serial_no.serial_no,
                    value: serial_no.serial_no,
                }));
        }
        addNewLine(data);
    }
};

// Check if item already exists and update quantity
const addItemIfExists = (data) => {
    let found = false;
    if (!base.pos_profile.custom_allow_add_new_items_on_new_line) {
        base.items.forEach((element, index) => {
            if (data.item_code === element.item_code && 
                ((data.has_batch_no && data.batch_no === (element.batch_no.value || element.batch_no)) || !data.has_batch_no)) {
                if (data.has_serial_no && data.serial_no) {
                    for (let serial of data.selected_serial_no) {
                        if (element.selected_serial_no.includes(serial)) {
                            return false;
                        }
                        addChild(base.items[index].selected_serial_no, data.selected_serial_no[0]);
                    }
                }
                base.items[index].qty += 1;
                found = true;
                priceListResource.fetch({ items: base.items[index] })
                .then(response => {
                    base.items[index].price_list_rate = response.children[0].price_list_rate
                    base.items[index].has_margin= response.children[0].has_margin
                    base.items[index].discount_percentage= response.children[0].discount_percentage
                    base.items[index].discount_amount = response.children[0].discount_amount 
                    base.items[index].validate_applied_rule = response.children[0].validate_applied_rule
                    base.items[index].price_or_product_discount = response.children[0].price_or_product_discount
                    base.items[index].pricing_rule_for = response.children[0].pricing_rule_for
                    base.items[index].margin_type = response.children[0].margin_type
                    base.items[index].margin_rate_or_amount = response.children[0].margin_rate_or_amount
                    base.items[index].has_pricing_rule = response.children[0].has_pricing_rule
                    base.items[index].pricing_rules = response.children[0].pricing_rules
                    base.items[index] = calculateRate(base.items[index]);
                    
                })
                .catch(error => {
                });
                

            }
        });
    }
    return found;
};

// Add new line item
const addNewLine = (data) => {
    priceListResource.fetch({ items: data })
                .then(response => {
                    data.price_list_rate = response.children[0].price_list_rate
                    data.has_margin= response.children[0].has_margin
                    data.discount_percentage= response.children[0].discount_percentage
                    data.discount_amount = response.children[0].discount_amount 
                    data.validate_applied_rule = response.children[0].validate_applied_rule
                    data.price_or_product_discount = response.children[0].price_or_product_discount
                    data.pricing_rule_for = response.children[0].pricing_rule_for
                    data.margin_type = response.children[0].margin_type
                    data.margin_rate_or_amount = response.children[0].margin_rate_or_amount
                    data.has_pricing_rule = response.children[0].has_pricing_rule
                    data.pricing_rules = response.children[0].pricing_rules
                    data = calculateRate(data);
                    
                })
                .catch(error => {
                });
    base.items.push(data);
};

const addChild = (data, value) => {
    data.push(value);
};

const calculateRate = (data) => {
    data.rate =   data.price_list_rate - ((data.discount_percentage * data.price_list_rate) / 100)
    data.amount= data.rate * data.qty
    return data;
    };
</script>