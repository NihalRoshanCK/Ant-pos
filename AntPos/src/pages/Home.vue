<template>
  <div class="w-screen h-screen">
    <div v-if="currentComponent">
        <component :is="currentComponent" />
    </div>
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
          <div class=" w-full p-2">
            <div class="w-full flex">
              <div class="w-11/12">
                <Autocomplete
                :options="computedOptions"
                v-model="selected_customer"
                placeholder="Select person"
                @update:modelValue="handleCustomer"
                />
              </div>
              <div class="w-1/12 flex justify-center items-center">
                <Button
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
                  @click="openCustomerForm"
                  />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import Navbar from '../component/Navbar.vue';
  import { FormControl, FeatherIcon, Autocomplete, createListResource ,Button } from 'frappe-ui';
  import { computed, inject, ref , watch } from 'vue';
  import { useDynamicComponent } from '../utils/Dialog';

  let base = inject('base');
  const { currentComponent, loadComponent } = useDynamicComponent();

  if (!base.Ant_Opening_Shift.name) {
    loadComponent('OpenShift');
  }
  const selected_customer = ref('');
  
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

