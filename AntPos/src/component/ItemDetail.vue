<template>
    <div class="w-1/2 h-full select-none">
        <div class="flex gap-4 h-[4%]">
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
        <div class="py-2 pr-3 h-[76%] overflow-y-scroll">
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
</template>

<script setup>

    import Customer from './Customer.vue';
    import { Button, FeatherIcon } from 'frappe-ui';
    import { inject } from 'vue';
    import item from './item.vue';

    const { loadComponent } = inject('dynamicComponent');
    let base = inject('base');
</script>