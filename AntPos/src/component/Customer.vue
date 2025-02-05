<template>
  <div class="w-11/12">
    <Autocomplete
      ref="autocompleteRef"
      :options="computedOptions"
      v-model="selected_customer"
      placeholder="Select person"
      @update:modelValue="handleCustomer"
    />
  </div>
</template>

<script setup>
import { ref, computed, inject, watch, nextTick, onMounted } from 'vue';
import Autocomplete from './custom_components/Autocomplete.vue';
import { createListResource } from 'frappe-ui';
import emitter from '/src/utils/emitter.js'; // Correct import statement

const selected_customer = ref('');
const autocompleteRef = ref(null);
const { loadComponent } = inject('dynamicComponent');
let base = inject('base');

// Define the customer list resource
const customerResource = createListResource({
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

// Compute the options for the autocomplete list
const computedOptions = computed(() => {
  return customerResource?.data
    ? customerResource.data.map((option) => ({
        mobile_no: option.mobile_no || '',
        label: option.label || 'Unnamed',
        value: option.value,
      }))
    : [];
});

// Handle the customer form
const handleCustomerForm = () => {
  autocompleteRef.value.closeOptions();
  nextTick(() => {
    loadComponent('CustomerForm');
  });
};

// Watch for changes in the selected customer
watch(
  selected_customer, (newValue, oldValue) => {
    if (newValue?.value && newValue.value !== oldValue?.value && newValue.value !== '') {
      base.customer = newValue.value;
    }
  }
);

// Listen to the event to refetch data and set the selected customer
onMounted(() => {
  emitter.on('customer-created', (customerData) => {
    customerResource.fetch().then(() => {
      selected_customer.value = {
        label: customerData.name,
        value: customerData.name
      };
    }).catch(error => {
      console.error('Error fetching customer data:', error);
    });
  });
});
</script>