<template>
    <div class="w-1/2 h-full select-none flex flex-col gap-2">
        <div class="h-[80%] w-full rounded-lg shadow-2xl px-2 pt-2">
            <div class="flex gap-4 h-[5%]">
                <Customer />
                <Button
                    class="w-1/12"
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
                    @click="loadComponent('CustomerForm');"
                    />
                </Button>
            </div>
            <div class="py-2 pr-3 h-[93%] overflow-y-scroll ">
                <div class="mb-2">
                    <div class="flex bg-gray-200 w-full py-2 px-3 justify-between rounded text-center ">
                        <div class="w-[18.4%]">
                            Item Code
                        </div>
                        <div  class="w-[18.4%]">
                            QTY
                        </div>
                        <div  class="w-[18.4%]">
                            UOM
                        </div>
                        <div  class="w-[18.4%]">
                            Rate
                        </div>
                        <div  class="w-[18.4%]">
                            Amount
                        </div>
                        <div class="w-[8%]">
                            Remove
                        </div>
                    </div>
                </div>
                <div v-for="(item, key) in base.items" :key="key" class="flex flex-col justify-between mb-2 ">
                    <item :item="item" :index="key"  />                   
                </div>
            </div>
        </div>

        <div class="h-[20%] flex shadow-2xl rounded">
            <div class=" w-[60%] grid grid-cols-2 gap-4 p-4 h-full">
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Total Qty"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Additional Discount"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Item Discount"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Placeholder"
                    :disabled="false"
                    label="Label"
                    v-model="inputValue"
                />

            </div>
            <div class=" w-[40%] h-full grid grid-cols-2 gap-2 p-4">
                <Button
                    :ref_for="true"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                    class="bg-orange-600 text-yellow-50"
                >
                    HELD
                </Button>
                <Button
                    :ref_for="true"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                    class="bg-cyan-600 text-yellow-50"
                    
                >
                    RETURN
                </Button>
                <Button
                    :ref_for="true"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                    class="bg-violet-600 text-yellow-50"
                >
                    SAVE/NEW
                </Button>
                <Button
                    :ref_for="true"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                    class="bg-green-600 text-yellow-50"
                >
                    PAY
                </Button>
                <Button
                    :ref_for="true"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                    class="bg-teal-600 text-yellow-50"
                >
                    PRINT DRAFT
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>

    import Customer from './Customer.vue';
    import { Button, FeatherIcon , FormControl } from 'frappe-ui';
    import { inject } from 'vue';
    import item from './item.vue';

    const { loadComponent } = inject('dynamicComponent');
    let base = inject('base');
</script>