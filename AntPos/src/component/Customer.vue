<template>
  <div class="w-11/12">
    <Autocomplete
      ref="autocompleteRef"
      :options="computedOptions"  
      v-model="selected_customer" 
      placeholder="Select person"
      @update:modelValue="handleCustomer"
    >
      <!-- <template #suffix>
        <FeatherIcon
          class="w-4"
          name="plus"
          @click="handleCustomerForm"
        />
      </template> -->
    </Autocomplete>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch, nextTick } from 'vue';
import Autocomplete from './custom_components/Autocomplete.vue';
import { createListResource, FeatherIcon } from 'frappe-ui';

const selected_customer = ref('');
const autocompleteRef = ref(null); // Create a reference for the Autocomplete component
const { currentComponent, loadComponent } = inject('dynamicComponent');
let base = inject('base');

let customer = createListResource({
  doctype: 'Customer',
  fields: ['name', 'mobile_no'],
  filters: {
    disabled: false,
  },
  pageLength: Number.MAX_VALUE * 2,
  auto: true,
  transform: (data) => {
    return data.map((item) => ({
      label: item.name,
      value: item.name,
      mobile_no: item.mobile_no,
    }));
  },
});

const computedOptions = computed(() => {
  return customer?.data
    ? customer.data.map((option) => ({
        mobile_no: option.mobile_no || '',
        label: option.label || 'Unnamed',
        value: option.value,
      }))
    : [];
});

const handleCustomerForm = () => {
  // Close the options first
  autocompleteRef.value.closeOptions();

  // Use nextTick to ensure the DOM updates are completed
  nextTick(() => {
    loadComponent('CustomerForm');
  });
};

watch(
  selected_customer, (newValue, oldValue) => {        
    if (newValue.value && newValue.value !== oldValue.value && newValue.value !== '') {
      base.customer = newValue.value;
    }
  }
);
</script>