<template>
  <div class="w-11/12">
    <Autocomplete
    :options="computedOptions"
    v-model="selected_customer"
    placeholder="Select person"
    @update:modelValue="handleCustomer"
    />
  </div>
</template>

<script setup>
    import { Autocomplete, createListResource } from 'frappe-ui';
    import { computed, inject, ref , watch } from 'vue';

    const selected_customer = ref('');

    let base = inject('base');;
    
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
            number: option.mobile_no || 'N/A',
            label: option.label || 'Unnamed',
            value: option.value,
          }))
        : [];
    });

    watch(
      selected_customer, (newValue, oldValue) => {
        if (newValue.value!=oldValue.value){
          base.customer=newValue.value
        }
      }
    )
</script>