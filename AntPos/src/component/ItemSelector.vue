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
                    @keyup.enter="debouncedSearchResource"
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
    import { ref , inject  } from 'vue';

    const debounceSearch = ref('');
    const items = ref([]);
    let base = inject('base');
    
    // Debounce function
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        };
    };

    const searchResource = () => {
        if (!base.customer){
            return console.log('Please select a customer');
        }
        createResource({
            url: 'ant_pos.ant_pos.api.item.items',
            method: 'GET',
            auto: true,
            makeParams() {
                return {
                    search_value: debounceSearch.value, 
                    pos_profile: JSON.stringify(base.pos_profile),
                    customer: base.customer
                };
            },
            onSuccess(data) {
                addItem(data);
                debounceSearch.value = '';
            },
            onError(error) {
                console.error('Search error:', error);
            },
        });
    };

    // Debounced version of searchResource
    const debouncedSearchResource = debounce(searchResource, 300);
    
    const addItem = (data) => {
        let find = false;
        data.open = false;

        find = differentiate(data, find);

        if (find) {
            return;
        }

        if (data.has_batch_no && data.batch_no) {
            data.serial_no_options = data.serial_no
                .filter(serial_no => data.batch_no && serial_no.batch_no === data.batch_no)
                .map(serial_no => (
                    {                    
                        label: serial_no.serial_no,
                        value: serial_no.serial_no,
                    }
                ));
        }

        addNewLine(data);
    };

    const differentiate = (data, find) => {
        if (!base.pos_profile.custom_allow_add_new_items_on_new_line) {
            base.items.forEach((element, index) => {
                if (data.item_code === element.item_code && ((data.has_batch_no && data.batch_no === element.batch_no) || !data.has_batch_no)) {
                    if (data.has_serial_no && data.serial_no) {
                        for (let serial of data.selected_serial_no) {
                            if (element.selected_serial_no.includes(serial)) {
                                return; 
                            }
                            addchild(base.items[index].selected_serial_no, data.selected_serial_no[0]);
                        }
                    }
                    base.items[index].qty += 1;
                    find = true;
                }
            });
        }
        return find;
    };

    const addNewLine = (data) => {
        base.items.push(data);
    };

    const addchild = (data, value) => {
        data.push(value);
    };
    const rateCalculation = (data) =>{
        return data.price_list_rate - ( (data.discount_percentage * data.price_list_rate)/100)
    }

</script>