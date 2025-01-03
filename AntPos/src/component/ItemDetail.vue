<template>
    <div class="w-1/2">
        <div class="flex gap-4">
            <Customer />
            <Button
                class="w-1/12"
                @click="loadComponent('CustomerForm');"
                :variant="'solid'"
                :ref_for="true"
                theme="gray"
                size="sm"
                label="Button"
                :loading="false"
                :loadingText="null"
                :disabled="false"
                :link="null"
            >
                <FeatherIcon
                class="w-4 cursor-pointer"
                name="plus"
                @click="loadComponent('CustomerForm');"
                />
            </Button>
        </div>
        <div class="p-2">
            <div v-for="(item, key) in base.items" :key="key" class="flex flex-col justify-between">
                <div class="flex  bg-gray-200 w-full py-2 px-3 rounded-t-2xl rounded-r-none rounded-l-none justify-between hover:cursor-pointer">
                    <div class="flex items-center">
                        <FeatherIcon name="chevron-down" class="w-5 h-5" />
                    </div>
                    <div>
                        {{ item.item_code }}
                    </div>
                    <div>
                        {{ item.qty }}
                    </div>
                    <div>
                        {{ item.uom }}
                    </div>
                    <div>
                        {{ item.rate }}
                    </div>

                </div>
                <div class="flex flex-col  bg-gray-200 w-full py-1 px-3 rounded-b-2xl  justify-between ">
                    <div class="grid grid-cols-3 w-full gap-4">
                        <div class="p-2">
                            <FormControl
                                :type="'text'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Item Code"
                                :disabled="true"
                                label="Item Code"
                                v-model="item.item_code"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="QTY"
                                :disabled="false"
                                label="QTY"
                                v-model="item.qty"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'text'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="UOM"
                                :disabled="false"
                                label="UOM"
                                v-model="item.uom"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Rate"
                                :disabled="false"
                                label="Rate"
                                v-model="item.rate"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Discount Percentage"
                                :disabled="false"
                                label="Discount Percentage"
                                v-model="item.discount_percentage"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Discount Amount"
                                :disabled="false"
                                label="Discount Amount"
                                v-model="item.discount_amount"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'text'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Price List Rate"
                                :disabled="false"
                                label="Price List Rate"
                                v-model="item.price_list_rate"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Available QTY"
                                :disabled="false"
                                label="Available QTY"
                                v-model="item.available_qty"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'text'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Group"
                                :disabled="true"
                                label="Group"
                                v-model="item.item_group"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Stock Qty"
                                :disabled="true"
                                label="Stock Qty"
                                v-model="item.stock_qty"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'text'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Stock UOM"
                                :disabled="true"
                                label="Stock UOM"
                                v-model="item.stock_uom"
                            />
                        </div>
                        <div class="p-2">
                            <FormControl
                                :type="'number'"
                                :ref_for="true"
                                size="sm"
                                variant="subtle"
                                placeholder="Serial No Qty"
                                :disabled="true"
                                label="Serial No Qty"
                                v-model="item.stock_qty"
                            />
                        </div>
                    </div>
                    <div class="w-full">
                        <div class="p-2">
                            <Autocomplete
                                :options=getserialNo(item.serial_no)
                                placeholder="Serial No"
                                :multiple="true"
                                v-model="item.selected_serial_no"
                            />
                        </div>
                        <div class="grid grid-cols-2 w-full gap-4">
                            <div class="p-2">
                                <FormControl
                                    :type="'number'"
                                    :ref_for="true"
                                    size="sm"
                                    variant="subtle"
                                    placeholder="Batch No Available QTY"
                                    :disabled="false"
                                    label="Batch No Available QTY"
                                    v-model="item.stock_qty"
                                />
                            </div>
                            <div class="p-2">
                                <FormControl
                                    :type="'number'"
                                    :ref_for="true"
                                    size="sm"
                                    variant="subtle"
                                    placeholder="Batch No Expire Date"
                                    :disabled="false"
                                    label="Batch No Expire Date"
                                    v-model="item.stock_qty"
                                />
                            </div>
                        </div>
                        <div>
                            <div class="p-2">
                                <Autocomplete
                                    :type="'select'"
                                    :options=getbatchNo(item.batch_nos)
                                    size="sm"
                                    variant="subtle"
                                    placeholder="Batch No"
                                    :disabled="false"
                                    label="Batch No "
                                    v-model="item.batch_no"
                                    :hideSearch="true"
                                />
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import Customer from './Customer.vue';
    import { Button, FeatherIcon , FormControl , Autocomplete } from 'frappe-ui';
    import { inject,computed,ref } from 'vue';
    const single= ref('1');

    const { currentComponent, loadComponent } = inject('dynamicComponent');
    let base = inject('base');    
    console.log(base.items,"base items")    ;
    
    const baseItems = computed(() => {
    // Return only object keys dynamically added to the Proxy
    return Object.entries(base.items || {}).reduce((acc, [key, value]) => {
        if (typeof value === 'object' && value !== null) {
            acc[key] = value;
        }
        return acc;
    }, {});
});
const getserialNo = (serial_nos) => {
    return serial_nos.map((serial_no) => {
        return {
            label: serial_no.serial_no,
            value: serial_no.serial_no,
        };
    });
}
const getbatchNo = (batch_nos) => {
    return batch_nos.map((batch_no) => {
        return {
            label: batch_no.batch_no,
            value: batch_no.batch_no,
        };
    });
    

}

    </script>