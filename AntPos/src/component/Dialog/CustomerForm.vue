<template>
    <Dialog  :options="{ size: '2xl' }" v-model="dialogVisible" @close="handleDialogClose" @after-leave="handleDialogClose">
      <template #body-title>
        <h3>Create Customer</h3>
      </template>
  
      <template #body-content>
        <div class="grid grid-cols-2 gap-5 w-full place-items-stretch">
          <!-- Customer Name -->
          <FormControl
            type="text"
            label="Customer Name"
            v-model="customer.customer_name"
            placeholder="Enter Customer Name"
            size="sm"
          />
  
          <!-- Mobile Number -->
          <FormControl
            type="text"
            label="Mobile Number"
            v-model="customer.mobile_no"
            placeholder="Enter Mobile Number"
            size="sm"
          />
  
          <!-- Email ID -->
          <FormControl
            type="email"
            label="Email ID"
            v-model="customer.email_id"
            placeholder="Enter Email ID"
            size="sm"
          />
  
          <!-- Gender -->
          <FormControl
            type="autocomplete"
            label="Gender"
            v-model="customer.gender"
            :options="genderOptions"
            placeholder="Select Gender"
            size="sm"
            
          />

      <!-- Customer Type
      <FormControl
          type="select"
          label="Customer Type"
          v-model="customer.customer_type"
          :options="customerTypeOptions"
          placeholder="Select Customer Type"
          size="sm"
        />
   -->
          <!-- Customer Group -->
          <FormControl
            type="autocomplete"
            label="Customer Group"
            v-model="customer.customer_group"
            :options="customerGroupsOptions"
            placeholder="Select Customer Group"
            size="sm"
          />
  
          <!-- Territory -->
          <FormControl
            type="autocomplete"
            label="Territory"
            v-model="customer.territory"
            :options="territoryOptions"
            placeholder="Select Territory"
            size="sm"
          />
        </div>
      </template>
  
      <template #actions>
        <Button variant="solid" @click="createCustomer">Submit</Button>
        <Button class="ml-2" @click="handleDialogClose">Close</Button>
      </template>
    </Dialog>
  </template>
  
  

  <script setup>
  import { ref, computed } from 'vue';
  import { Dialog, createListResource, Button, FormControl, createResource } from 'frappe-ui';
  import { inject } from 'vue';
  
  // Reactive state for dialog visibility
  const dialogVisible = ref(true);
  const base = inject('base');
  
  const { currentComponent, loadComponent } = inject('dynamicComponent');
  
  // Customer object
  const customer = ref({
    customer_name: '',
    mobile_no: '',
    email_id: '',
    gender: '',
    customer_type: 'Individual',
    customer_group:"",
    territory: '',
    posa_referral_company:base.pos_profile.company,
    gst_category:"Unregistered",


  });
  // Customer Type Options
const customerTypeOptions = [
  { label: 'Individual', value: 'Individual' },
  { label: 'Company', value: 'Company' },
];





  // Fetching options for dropdowns
  const genderOptionsResource = createListResource({
    doctype: 'Gender',
    fields: ['name'],
    pageLength: 10,
    auto: true,
    transform: (data) => data.map((item) => item.name),
  });
  
  const territoryOptionsResource = createListResource({
    doctype: 'Territory',
    fields: ['name'],
    filters: { is_group: 0 },
    pageLength: 5000,
    orderBy: 'name',
    auto: true,
   transform: (data) => data.map((item) => item.name),
  });
  
  const customerGroups = createListResource({
    doctype: 'Customer Group',
    fields: ['name'],
    filters: { is_group: 0 },
    pageLength: 1000,
    orderBy: 'name',
    auto: true,
    transform: (data) => data.map((item) => item.name),
  });
  
  // Computed options for dropdowns
  const genderOptions = computed(() => genderOptionsResource.data || []);
  const customerGroupsOptions = computed(() => customerGroups.data || []);
  const territoryOptions = computed(() => territoryOptionsResource.data || []);
  
  // Function to close the dialog
  const handleDialogClose = () => {
    dialogVisible.value = false;
  };
  
  // Function to handle customer submission
  const createCustomer = () => {
    // console.log('Creating Customer:', customer.value);
    
    const customerData = {
  ...customer.value,
  gender: customer.value.gender?.value ?? null,
  customer_group: customer.value.customer_group?.value ?? null,
  territory: customer.value.territory?.value ?? null
};
    
console.log('Customer Data:', customerData);
    createResource({
      method: 'POST',
      url: '/api/resource/Customer',
      auto: true,
      makeParams() {
        return {
          data: customerData, // Pass customer data directly
        };
      },
      onSuccess(data) {
        console.log('Customer Created:', data);
        handleDialogClose(); // Close the dialog after successful submission
      },
      onError(err) {
        console.error('Error:', err);
      },
    });
  };
  </script>
  