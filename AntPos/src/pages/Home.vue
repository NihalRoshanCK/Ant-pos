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
    v-model="debounceSearch"
    placeholder="Search Items"
    size="sm"
    variant="subtle"
  >
    <template #prefix>
      <FeatherIcon
        class="w-4"
        name="search"
      />
    </template>
  </FormControl>




   



  <div>
  <!-- No items found message -->
  <div v-if="items.length === 0" class="text-center text-gray-500">
    No items found. Try searching again.
  </div>

  <!-- Items display -->
  <div v-else >
    <div class="flex justify-between items-center border-b pb-4">
      <div class="flex justify-between w-full">
        <span class="text-lg font-medium mr-4">{{ items.item_code }}</span>
        <span class="text-sm text-gray-500">Qty: 1</span>
        <span class="text-sm text-gray-500">price: {{ items.rate }}</span>
        <span class="text-lg font-semibold ml-4">{{ items.serial_no }}</span>
      </div>
    </div>
  </div>
</div>




















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
    import { computed, inject, ref , watch,  } from 'vue';
    import {  createResource } from 'frappe-ui';
    import { useDynamicComponent } from '../utils/Dialog';

    let base = inject('base');
    const { currentComponent, loadComponent } = useDynamicComponent();
    const debounceSearch = ref('');
    const items = ref([]);
console.log(items,"1167.")
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




  // Create a resource with debounce
  const searchResource = createResource({
    url: 'ant_pos.ant_pos.api.pos_profile.get_items ',
    method: 'POST',
    debounce: 500, // Delay of 500ms
    makeParams() {
      return {
      search_value: debounceSearch.value, // Use the search input value
      pos_profile:base.pos_profile
      };
    },
    onSuccess(data) {
      console.log(data, 'Search results');
      items.value = data || [];
      console.log('Updated items:', items.value); // Log updated items
    },
    onError(error) {
      console.error('Search error:', error);
    },
  });

  // Watch for changes in search input and trigger the resource
  watch(debounceSearch, (newVal) => {
    console.log('Debounce search value:', newVal); // Debug log
    if (newVal) {
      searchResource.fetch();
    }
  });

  </script>

