<template>
    <div class="w-1/2">
        <div class="flex gap-8">
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
        <div>
            <div v-for="item in base.items" class="flex justify-between">
                <div>
                    {{ item.item_code }}
                </div>
                <div>
                    {{ item.rate }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import Customer from './Customer.vue';
    import { useDynamicComponent } from '../utils/Dialog';
    import { Button, FeatherIcon } from 'frappe-ui';
    import { inject } from 'vue';

    const { currentComponent, loadComponent } = inject('dynamicComponent');
    let base = inject('base');

</script>