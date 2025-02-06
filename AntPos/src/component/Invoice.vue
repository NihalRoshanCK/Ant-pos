<template>
    <div class="w-1/2 shadow-2xl pt-2 px-2 rounded">
        <div class="h-[85%]  w-full ">
            <div class=" grid grid-cols-2 gap-4 p-2">
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Placeholder"
                    :disabled="false"
                    label="Label"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Placeholder"
                    :disabled="false"
                    label="Label"
                    v-model="inputValue"
                />

            </div>
            
            <div class=" grid grid-cols-2 gap-4 p-2 items-center" v-for="mode in base.pos_profile.payments">
                    <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    :label="mode.mode_of_payment"
                    v-model="inputValue"
                />
                <Button
                        class="w-full h-full"
                        :variant="'solid'"
                        :ref_for="true"
                        theme="gray"
                        size="lg"
                        label="Button"
                        :loading="false"
                        :loadingText="null"
                        :disabled="false"
                        :link="null"
                    >
                        {{mode.mode_of_payment}}
                    </Button>

            </div>
            <div class=" grid grid-cols-2 gap-4 p-2">
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Net Total"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Tax and Charges"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Total Amount"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Discount Amount"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Grand Total"
                    v-model="inputValue"
                />
                <FormControl
                    :type="'search'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Rounded Total"
                    v-model="inputValue"
                />
            </div>
        </div>
        <div class="h-[15%] w-full mt-2">
            <div class="h-1/2">
                <div class="flex gap-8 h-full">
                    <Button
                        class="w-1/2 h-full"
                        :variant="'solid'"
                        :ref_for="true"
                        theme="gray"
                        size="lg"
                        label="Button"
                        :loading="false"
                        :loadingText="null"
                        :disabled="false"
                        :link="null"
                    >
                        Button
                    </Button>
                    <Button
                        class="w-1/2 h-full"
                        :variant="'solid'"
                        :ref_for="true"
                        theme="gray"
                        size="lg"
                        label="Button"
                        :loading="false"
                        :loadingText="null"
                        :disabled="false"
                        :link="null"
                    >
                        Button
                    </Button>
                </div>
            </div>
            <div class="h-1/2">
                <Button
                    class="w-full"
                    :variant="'solid'"
                    :ref_for="true"
                    theme="gray"
                    size="lg"
                    label="Button"
                    :loading="false"
                    :loadingText="null"
                    :disabled="false"
                    :link="null"
                >
                    Button
                </Button>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { Button, FeatherIcon , FormControl , createResource } from 'frappe-ui';
    import { inject,watch } from 'vue';
    let base = inject('base');

</script>