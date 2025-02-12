<template>
    <div class="w-1/2 shadow-2xl pt-2 px-2 rounded">
        <div class="h-[85%]  w-full ">
            <div class=" grid grid-cols-2 gap-4 p-2">
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Placeholder"
                    :disabled="true"
                    label="Amount Paid"
                    v-model="base.invoice.rounded_total" 
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="Placeholder"
                    :disabled="true"
                    label="To Be Paid"
                    v-model="base.invoice.rounded_total"
                />
            </div>
            <div class=" grid grid-cols-2 gap-4 p-2 items-center" v-for=" ( mode , index) in base.pos_profile.payments">
                <FormControl
                    v-if="base.invoice?.payments && base.invoice.payments[index]"
                    type="number"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    :label="mode.mode_of_payment"
                    v-model="base.invoice.payments[index].amount"
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
                        @click="changemode(index)"
                    >
                        {{mode.mode_of_payment}}
                    </Button>
            </div>
            <div class=" grid grid-cols-2 gap-4 p-2">
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Net Total"
                    v-model="base.invoice.net_total"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Tax and Charges"
                    v-model="base.invoice.total_taxes_and_charges"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Total Amount"
                    v-model="base.invoice.total"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Discount Amount"
                    v-model="base.invoice.discount_amount"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Grand Total"
                    v-model="base.invoice.grand_total"
                />
                <FormControl
                    :type="'number'"
                    :ref_for="true"
                    size="sm"
                    variant="subtle"
                    placeholder="0"
                    :disabled="false"
                    label="Rounded Total"
                    v-model="base.invoice.rounded_total"
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
                        @click="test"
                    >
                        Submit
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
                        Submit & Print
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
                    Cancel
                </Button>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { Button , FormControl ,createResource  ,createDocumentResource } from 'frappe-ui';
    import { inject , onMounted, watchEffect } from 'vue';
    let base = inject('base');
    const addPayments = () => {
        base.pos_profile.payments.forEach(element => {
            if (!base.invoice.payments.some(payment => payment.mode_of_payment === element.mode_of_payment)) {
                base.invoice.payments.push({
                    "mode_of_payment": element.mode_of_payment,
                    "amount": element.default ? base.invoice.base_rounded_total : 0.00,
                    "base_amount": 0.00
                });
            }
        });
    };
    const changemode = (index) => {
    base.invoice.payments[index].amount = 
        base.invoice.payments[index].amount === base.invoice.base_rounded_total ? 0 : base.invoice.base_rounded_total;
    };
    onMounted(() => {
        addPayments()
    });
    let post = createDocumentResource({
        doctype: 'Sales Invoice',
        name: base.invoice.name,
    })
    let test1 = createResource({
        url: 'ant_pos.ant_pos.api.item.submitDoc',
        method: 'POST',
        makeParams() {
            return {
                doc:'Sales Invoice',
                name:base.invoice.name
            };
        },
    });
    const test=()=>{
        console.log(base.invoice);
        post.setValue.submit({
            payments: base.invoice.payments,
            base_write_off_amount:0.00
        }) 
        // post.submit()
        test1.fetch()
    }
</script>