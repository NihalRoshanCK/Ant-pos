<template>
    <div :class="['flex bg-gray-200 w-full py-2 px-3 justify-between hover:cursor-pointer text-center' ,items.open ? 'rounded-t-2xl' : 'rounded']">
        <div class="flex items-center h-[100%] rounded hover:bg-gray-300" @click="items.open = !items.open">
            <FeatherIcon :name="items.open ? 'chevron-up' : 'chevron-down'" class="w-5 h-5" />
        </div>
        <div class="w-[18.4%]">
            {{ items.item_code }}
        </div>
        <div class="w-[18.4%]">
            {{ items.qty }}
        </div>
        <div class="w-[18.4%]">
            {{ items.uom }}
        </div>
        <div class="w-[18.4%]">
            {{ items.rate > 0 ? items.rate.toFixed(2) : 0 }}
        </div>
        <div class="w-[18.4%]">
            {{ items.amount ? items.amount.toFixed(2) : '0.00' }}
        </div>
        <div class="w-[8%] flex items-center justify-center">
            <FeatherIcon name="trash-2" class="w-5 h-5 rounded hover:bg-red-400 fill-red-700" @click="base.items.splice(index, 1)" />
        </div>
    </div>
    <div v-if="items.open" class="flex flex-col bg-gray-200 w-full py-1 px-3 rounded-b-2xl justify-between">
        <div class="grid grid-cols-3 w-full gap-4">
            <div class="p-2">
                <FormControl
                    type="text"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="items Code"
                    :disabled="true"
                    label="items Code"
                    v-model="items.item_code"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="QTY"
                    v-model="items.qty"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="text"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="UOM"
                    :disabled="false"
                    label="UOM"
                    v-model="items.uom"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    :disabled="false"
                    label="Rate"
                    placeholder="0"
                    v-model="items.rate"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Discount Percentage"
                    :disabled="false"
                    label="Discount Percentage"
                    v-model="items.discount_percentage"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    :disabled="false"
                    label="Discount Amount"
                    placeholder="0"
                    v-model="items.discount_amount"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="text"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    :disabled="false"
                    label="Price List Rate"
                    placeholder="0"
                    v-model="items.price_list_rate"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Available QTY"
                    :disabled="false"
                    label="Available QTY"
                    v-model="items.available_qty"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="text"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Group"
                    :disabled="true"
                    label="Group"
                    v-model="items.item_group"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Stock Qty"
                    :disabled="true"
                    label="Stock Qty"
                    v-model="items.stock_qty"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="text"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Stock UOM"
                    :disabled="true"
                    label="Stock UOM"
                    v-model="items.stock_uom"
                />
            </div>
            <div class="p-2">
                <FormControl
                    type="number"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Serial No Qty"
                    :disabled="true"
                    label="Serial No Qty"
                    v-model="items.stock_qty"
                />
            </div>
        </div>
        <div class="w-full">
            <div class="p-2">
                <Autocomplete
                    :options="items.serial_no_options"
                    placeholder="Serial No"
                    :multiple="true"
                    v-model="items.selected_serial_no"
                />
            </div>
            <div class="grid grid-cols-2 w-full gap-4">
                <div class="p-2">
                    <FormControl
                        type="number"
                        :ref_for="true"
                        size="sm"
                        variant="subtle"
                        placeholder="Batch No Available QTY"
                        :disabled="false"
                        label="Batch No Available QTY"
                        v-model="items.stock_qty"
                    />
                </div>
                <div class="p-2">
                    <FormControl
                        type="number"
                        :ref_for="true"
                        size="sm"
                        variant="subtle"
                        placeholder="Batch No Expire Date"
                        :disabled="false"
                        label="Batch No Expire Date"
                        v-model="items.stock_qty"
                    />
                </div>
            </div>
            <div>
                <div class="p-2">
                    <Autocomplete
                        type="select"
                        :options="getbatchNo(items.batch_nos)"
                        size="sm"
                        variant="subtle"
                        placeholder="Batch No"
                        :disabled="false"
                        label="Batch No"
                        v-model="items.batch_no"
                        :hideSearch="true"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { FeatherIcon, FormControl, Autocomplete } from 'frappe-ui';
import { inject, watch, defineProps, onMounted, onUnmounted } from 'vue';

let base = inject('base');
const emitter = inject('emitter');

const props = defineProps({
    items: {
        type: Object,
        required: true,
    },
    index: {
        type: Number,
        required: true,
    },
});

const getbatchNo = (batch_nos) => {
    return batch_nos.map((batch_no) => ({
        label: batch_no.batch_no,
        value: batch_no.batch_no,
    }));
};

// Watch for changes in batch_no and update serial_no_options
watch(
    () => props.items.batch_no,
    (newBatchNo, oldBatchNo) => {
        if (newBatchNo && (newBatchNo.value !== oldBatchNo?.value) || !oldBatchNo) {
            props.items.selected_batch_no = newBatchNo.value;
            let find = validateitems(props.index);
            if (!find) {
                props.items.selected_serial_no = [];
                props.items.serial_no_options = props.items.serial_no.filter((serial_no) => props.items.selected_batch_no && serial_no.batch_no === props.items.selected_batch_no)
                    .map((serial_no) => ({
                        label: serial_no.serial_no,
                        value: serial_no.serial_no,
                    }));
            }
        }
    }
);

const validateitems = (place) => {
    if (!base.pos_profile.custom_allow_add_new_item_on_new_line) {
        let find = false;
        for (let index = 0; index < base.items.length; index++) {
            if (place !== index && base.items[place].item_code === base.items[index].item_code &&
                ((base.items[place].has_batch_no && base.items[index].batch_no === base.items[index].batch_no) || !base.items[place].has_batch_no)) {
                base.items[index].qty += base.items[place].qty;
                base.items.splice(place, 1);
                find = true;
                return find;
            }
        }
        return find;
    }
};

const calculateAmountTotal = () => {
    let total = 0;
    let discount = 0;
    base.items.forEach((element) => {
        element.amount = element.qty * element.rate;
        total += element.amount;
        discount+= element.discount_amount;
        
    });
    base.item_discount = discount.toFixed(2);
    base.total = (total - ((base.additional_discount || 0) )).toFixed(2);
};

const calculateQtyTotal = () => {
    let total = 0;

    base.items.forEach((element) => {
        total += element.qty || 0;
    });
    base.total_qty = total.toFixed ? total.toFixed(2) : '0.00';
};

const validateQty = (qty) => {
    const availableSerials = props.items.serial_no_options.map(option => option.value);
    if (qty > availableSerials.length) {
        console.log(
            availableSerials.length,
            'Qty is greater than available serial no'
        );
        // Update qty to maximum available serial no count
        props.items.qty = availableSerials.length;
        return true; // Indicate that the qty is now valid
    }
    return true;
};

watch(
    () => props.items.selected_serial_no,
    (newSerial, oldSerial) => {
        if (props.items.has_serial_no && newSerial !== oldSerial) {
            props.items.qty = newSerial.length;
            emitter.emit('fetchPriceList', props);
        }
    }
);

watch(
    () => props.items.qty,
    (newValue, oldValue) => {
        if (newValue !== oldValue) {
            if (!validateQty(newValue)) {
                // Do nothing here; validateQty has already updated props.items.qty.
                return;
            }
            adjustSerialNumbers(newValue, oldValue);
            props.items.rate = rateCalculation(props.items);
            props.items.amount = props.items.rate * props.items.qty;
            calculateQtyTotal();
        }
    }
);

const adjustSerialNumbers = (newQty, oldQty) => {
    if ( newQty > props.items.selected_serial_no.length) {
        const diff = newQty - oldQty;
        for (let i = 0; i < diff; i++) {
            if (!props.items.selected_serial_no.includes(props.items.serial_no_options[i])){
                props.items.selected_serial_no.push(props.items.serial_no_options[i].value);
            }
        }
        } else {
        props.items.selected_serial_no = props.items.selected_serial_no.slice(0, newQty);

    }
    
};

watch(
    () => props.items.discount_percentage,
    (newValue, oldValue) => {
        if (newValue !== oldValue || !oldValue) {
            
            props.items.rate = rateCalculation(props.items);
            props.items.amount = props.items.rate * props.items.qty;        
        }
    }
);

watch(
    () => props.items.discount_amount,
    (newValue, oldValue) => {
        if (newValue !== oldValue || !oldValue) {
            props.items.discount_percentage = (props.items.discount_amount / props.items.price_list_rate) * 100;
        }
    }
);

base.items.forEach((items) => {
    watch(
        () => items,
        () => {
            calculateAmountTotal();
        },
        { deep: true }
    );
});

const rateCalculation = (data) => data.price_list_rate - ((data.discount_percentage * data.price_list_rate) / 100);

// Listen for rateCalculated event and update items rate
onMounted(() => {
    props.items.rate = rateCalculation(props.items);
    props.items.amount = props.items.rate * props.items.qty;
    calculateQtyTotal();
    calculateAmountTotal();
});

onUnmounted(() => {
    calculateAmountTotal();
    calculateQtyTotal();
});
</script>