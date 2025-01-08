<template>
    <div :class="['flex bg-gray-200 w-full py-2 px-3 justify-between hover:cursor-pointer text-center' ,item.open ? 'rounded-t-2xl' : 'rounded']">
        <div  class="flex items-center h-[100%]  rounded hover:bg-gray-300 " @click="item.open=!item.open">
            <FeatherIcon :name="item.open ? 'chevron-up' : 'chevron-down'" class="w-5 h-5" />
        </div>
        <div  class="w-[22.5%]">
            {{ item.item_code }}
        </div>
        <div  class="w-[22.5%]">
            {{ item.qty }}
        </div >
        <div  class="w-[22.5%]">
            {{ item.uom }}
        </div>
        <div  class="w-[22.5%]">
            {{ item.rate }}
        </div>
        <div class="w-[8%]  flex items-center justify-center">
            <FeatherIcon name="trash-2"  class="w-5 h-5 rounded hover:bg-red-400  fill-red-700" @click="base.items.splice(key, 1)" />
        </div>

    </div>
    <div v-if="item.open" class="flex flex-col  bg-gray-200 w-full py-1 px-3 rounded-b-2xl  justify-between ">
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
                    :options=item.serial_no_options
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
                        label="Batch No"
                        v-model="item.batch_no"
                        :hideSearch="true"
                        />
                </div>
            </div>

        </div>
    </div>
</template>
<script setup>
import { Button, FeatherIcon, FormControl, Autocomplete } from 'frappe-ui';
import { inject, watch, defineProps } from 'vue';

let base = inject('base');

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  key: {
    type: Number,
    required: true,
  },
});

const getserialNo = (serial_nos, batch_no) => {
  if (!batch_no) return [];
  return serial_nos
    .filter((serial_no) => serial_no.batch_no === batch_no)
    .map((serial_no) => ({
      label: serial_no.serial_no,
      value: serial_no.serial_no,
    }));
};

const getbatchNo = (batch_nos) => {
  return batch_nos.map((batch_no) => ({
    label: batch_no.batch_no,
    value: batch_no.batch_no,
  }));
};

// Watch for changes in batch_no and update serial_no_options
watch(
  () => props.item.batch_no,
  (newBatchNo, oldBatchNo) => {
    if (newBatchNo && newBatchNo !== oldBatchNo) {
      console.log(`Batch No changed from ${oldBatchNo} to ${newBatchNo}`);
      props.item.selected_batch_no= newBatchNo.value;
      props.item.serial_no_options =  props.item.serial_no.filter((serial_no) =>  props.item.selected_batch_no && serial_no.batch_no ===  props.item.selected_batch_no)
                .map((serial_no) => ({
                    label: serial_no.serial_no,
                    value: serial_no.serial_no,
        }));
    } else {
      props.item.serial_no_options = [];
    }
  }
);
</script>