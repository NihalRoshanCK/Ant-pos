<template>
    <div class="w-1/2">
        <div>
            <div class="">
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
                    <div v-if="items.length === 0" class="text-center text-gray-500">
                        No items found. Try searching again.
                    </div>

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
</template>


<script setup>
    import { FormControl, FeatherIcon , createResource} from 'frappe-ui';
    import { ref , watch, inject  } from 'vue';
    const debounceSearch = ref('');
    const items = ref([]);
    let base = inject('base');
    const searchResource = () => {
        if (!base.customer){
            return console.log('Please select a customer');
            
        }
        createResource({
            url: 'ant_pos.ant_pos.api.item.items',
            method: 'GET',
            // debounce: 500, 
            auto:true,
            makeParams() {
                return {
                    search_value: debounceSearch.value, 
                    pos_profile:JSON.stringify(base.pos_profile),
                    customer:base.customer
                };
            },
            onSuccess(data) {
                // console.log(data, 'Search results');
                // items.value = data || [];
                // console.log('Updated items:', items.value);
                base.items.push(data)
                debounceSearch.value = '';
            },
            onError(error) {
                console.error('Search error:', error);

            },
        });

    }
    

    watch(debounceSearch, (newVal) => {
        console.log('Debounce search value:', newVal);
        if (newVal) {
        searchResource();
        }
    });
</script>