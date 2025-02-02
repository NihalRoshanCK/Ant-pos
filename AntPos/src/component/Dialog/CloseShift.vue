<template>
    <Dialog v-model="modelValue" @close="$emit('update:modelValue', false)">
        <template #body-title>
            <h3>ANT Closing Shift</h3>
        </template>

        <template #body-content>
            <table class="w-full mt-4">
                <thead>
                    <tr class="text-left text-sm border-b">
                        <th class="pb-2">Mode of Payment</th>
                        <th class="pb-2">Opening Amount</th>
                        <th class="pb-2">Closing Amount</th>
                        <th class="pb-2">Expected Amount</th>
                        <th class="pb-2">Difference</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(row, index) in rows" :key="index" class="border-b">
                        <td class="py-2 pr-4">{{ row.mode }}</td>
                        <td class="py-2 px-1">
                            <FormControl
                                type="number"
                                size="sm"
                                variant="subtle"
                                v-model="row.opening"
                                @input="calculateDifference(index)"
                            />
                        </td>
                        <td class="py-2 px-1">
                            <FormControl
                                type="number"
                                size="sm"
                                variant="subtle"
                                v-model="row.closing"
                                @input="calculateDifference(index)"
                            />
                        </td>
                        <td class="py-2 px-1">
                            <FormControl
                                type="number"
                                size="sm"
                                variant="subtle"
                                v-model="row.expected"
                            />
                        </td>
                        <td class="py-2 px-1">
                            <FormControl
                                type="number"
                                size="sm"
                                variant="subtle"
                                :value="row.difference"
                                disabled
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="flex justify-end gap-2 mt-4">
                <Button variant="ghost" @click="handleClose">Cancel</Button>
                <Button variant="solid" @click="handleSubmit">Submit</Button>
            </div>
        </template>

    
    </Dialog>

    <Button @click="dialog1 = true">Show Dialog</Button>
</template>

<script setup>
import { ref, reactive,defineProps, defineEmits } from 'vue';
import { Button, Dialog, FormControl } from 'frappe-ui';

const dialog1 = ref(false);
const rows = reactive([
    { mode: 'card/upi', opening: 0, closing: 0, expected: 0, difference: 0 },
    { mode: 'cash', opening: 0, closing: 0, expected: 0, difference: 0 },
    { mode: 'upi', opening: 0, closing: 0, expected: 0, difference: 0 },
]);

const calculateDifference = (index) => {
    rows[index].difference = rows[index].closing - rows[index].opening;
};



const props = defineProps({
  modelValue: Boolean
});

const emits = defineEmits(['update:modelValue']);

const handleSubmit = () => {
  // Handle submission
  emits('update:modelValue', false);
};

const handleClose =()=>
{
    emits('update:modelValue', false);
}


</script>
