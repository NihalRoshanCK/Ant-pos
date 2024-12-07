<template>
  <div class="w-screen h-screen">
    <div class="w-screen h-[6%]">
      <Navbar />
    </div>
    <div class="w-screen h-[94%] flex">
      <div class="w-1/2 ">
        <div>
          <div class="p-2">
            <FormControl
              type="text"
              placeholder="Search Items"
            >
              <template #prefix>
                <FeatherIcon
                  class="w-4"
                  name="search"
                />
              </template>
            </FormControl>
          </div>
        </div>
      </div>
      <div class="w-1/2">
        <div>
<div class="p-2">
  <!-- Container for Autocomplete and Plus Icon -->
  <div class="flex items-center space-x-2">
    <!-- Autocomplete Component -->
    <Autocomplete
      :options="computedOptions"
      v-model="single"
      placeholder="Select person"
      @update:modelValue="handleCustomer"
      class="flex-grow"
    />
    
    <!-- Feather Icon with Plus on the Right -->
    <FeatherIcon
      class="w-4 cursor-pointer"
      name="plus"
      @click="openCustomerForm"
    />
  </div>
</div>


          
        </div>
      </div>
    </div>
    <CustomerForm v-if="showCustomerForm" @close="closeCustomerForm"  />
  </div>
</template>

<script setup>
import Navbar from '../component/Navbar.vue';
import CustomerForm from '../component/Dialog/CustomerForm.vue'
import { FormControl, FeatherIcon, Autocomplete, createListResource ,Button } from 'frappe-ui';
import { computed, inject, ref } from 'vue';

// Injecting the 'base' object
let base = inject('base');

const showCustomerForm = ref(false);
const openCustomerForm = () => {
  showCustomerForm.value = true;
};
const closeCustomerForm = () => {
  showCustomerForm.value = false;
};


// Create the resource
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

const handleCustomer = (selected) => {
  console.log("Selected customer:", selected);

  // Set the selected customer in the base object
  if (base) {
    base.customer = selected.value;
    console.log("Customer set in base:", base.customer);
  } else {
    console.error("Base is not defined!");
  }
  console.log(base,"kkkkkkk");
  
};

const computedOptions = computed(() => {
  return customer?.data
    ? customer.data.map((option) => ({
        number: option.mobile_no || 'N/A',
        label: option.label || 'Unnamed',
        value: option.value,
      }))
    : [];
});

const single = ref('');
</script>

