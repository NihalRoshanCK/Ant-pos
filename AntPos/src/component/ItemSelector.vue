<template>
    <div class="w-1/2">
        <div>
            <div>
                <!-- Search Input -->
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

                <!-- Search Results -->
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
        console.log(data, "Search result data");
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
    auto: false, // Manual fetch
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
        console.log(data, "Add items data");
        
        addItem(data);
    },
});

const priceListResource = createResource({
    url: 'erpnext.stock.get_item_details.apply_price_list', // API endpoint
    method: 'POST', // Change to POST as most ERPNext APIs use POST
    debounce: 500,
    auto: false,
    makeParams() {
        return {
            args: JSON.stringify({
                items: [
                    {
                    "doctype": "Sales Invoice Item",
                    "name": "new-sales-invoice-item-lrdmbgmbcz",
                    "child_docname": "new-sales-invoice-item-lrdmbgmbcz",
                    "item_code": "SR-MWR-SRT-LINEN-HS",
                    "item_group": "SURPLUS PRODUCTS",
                    "brand": null,
                    "qty": 2,
                    "stock_qty": 2,
                    "uom": "Nos",
                    "stock_uom": "Nos",
                    "parenttype": "Sales Invoice",
                    "parent": "new-sales-invoice-owspmikswv",
                    "pricing_rules": [
                    "PRLE-0003"
                    ],
                    "is_free_item": 0,
                    "warehouse": "MG Road - FITPL",
                    "serial_no": "3030012506\n3030012508",
                    "batch_no": "B303001-24010-00010",
                    "price_list_rate": 1899,
                    "conversion_factor": 1,
                    "margin_type": "Percentage",
                    "margin_rate_or_amount": 0
                    }
                ],
                    "customer":base.customer.name,
                    "customer_group":  base.customer.customer_group,
                    "territory": "India",
                    "currency":base.pos_profile.currency,
                    "conversion_rate": 1,
                    "price_list": "Standard Selling",
                    "price_list_currency": "INR",
                    "plc_conversion_rate": 1,
                    "company": base.pos_profile.company,
                    "transaction_date": "",
                    "ignore_pricing_rule": 0,
                    "doctype": "Sales Invoice",
                    "name": "new-sales-invoice-owspmikswv",
                    "is_return": 0,
                    "update_stock": 1,
                    "pos_profile": "FORMOST MG Road",
                    "is_internal_customer": 0
            })
        };
    },
    onError(error) {
        console.error('Price list error:', error);
    },
    onSuccess(data) {
        console.log('Price list data:', data);
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
                            return true;
                        }
                        addChild(base.items[index].selected_serial_no, data.selected_serial_no[0]);
                    }
                }
                base.items[index].qty += 1;
                found = true;
                base.item
                // priceListResource.fetch({ items: base.items[index] });
                console.log("ooooooooooooooooooooooooooooooooo");
                
                priceListResource.fetch({ items: base.items[index] });

            }
        });
    }
    return found;
};

// Add new line item
const addNewLine = (data) => {
    base.items.push(data);
};

// Add child item
const addChild = (data, value) => {
    data.push(value);
};

// Calculate rate after discount
const calculateRate = (data) => {
    return data.price_list_rate - ((data.discount_percentage * data.price_list_rate) / 100);
};
</script>