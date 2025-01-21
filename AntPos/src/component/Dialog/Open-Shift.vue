<template>
    <Dialog v-model="dialog1"  @close="closeDialog">
      <template #body-title>
        <h3>Create ANT Opening Shift</h3>
      </template>
      <template #body-content>
        <div class="flex flex-col gap-8">
          <!-- Company Selection -->
          <FormControl
            type="autocomplete"
            :options="options.company.map(company => ({ label: company, value: company }))"
            size="sm"
            variant="subtle"
            placeholder="Select Company"
            label="Company"
            v-model="autocompleteValue"
            hide-search="true"
          />

          <!-- POS Profile Selection -->
          <FormControl
            type="autocomplete"
            :options="getProfileOptions()"
            size="sm"
            variant="subtle"
            placeholder="Select POS Profile"
            :disabled="!autocompleteValue"
            label="POS Profile"
            v-model="autocompleteProfileValue"
            hide-search="true"
          />

          <!-- Mode of Payment -->
          <div v-if="mode_of_payment.length">
            <div class="border-2">
              <div class="p-2 flex justify-between">
                <div class="text-center">Mode Of Payment</div>
                Opening Amount
              </div>
              <div
                class="flex justify-between p-2 border-t-2"
                v-for="mode in mode_of_payment"
                :key="mode"
              >
                <div class="w-1/2">{{ mode }}</div>
                <div class="">
                  <FormControl
                    type="number"
                    size="sm"
                    variant="subtle"
                    placeholder="Opening Amount"
                    :name="mode"
                    v-model="openingAmounts[mode]" 
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="solid" @click="confirmShift">Confirm</Button>
        <Button class="ml-2" @click="closeDialog">Close</Button>
      </template>
    </Dialog>
</template>


<script setup>
    import { createResource, Button, Dialog, FormControl } from 'frappe-ui';
    import { inject, ref, watch, reactive } from 'vue';

    const options = reactive({company: [],profile: {},});
    const dialog1 = ref(false);
    const autocompleteValue = ref({});
    const autocompleteProfileValue = ref({});
    const mode_of_payment = ref([]);
    const openingAmounts = reactive({});
    let base = inject('base');

    const closeDialog = () => {
        validate_pos.fetch()
    };
    const submit = createResource({
        url: 'ant_pos.ant_pos.api.pos_profile.create_opening',
        method: 'POST',
        
        onSuccess(data) {
        
        
        },
    });
    const confirmShift = async () => {
      const submissionData = {
          company: autocompleteValue.value.value || null,
          pos_profile: autocompleteProfileValue.value.value || null,
          status: 'Open',
          opening_balance_details: mode_of_payment.value.map((mode) => ({
          mode_of_payment: mode,
          opening_amount: openingAmounts[mode] || 0,
          })),
      };

      try {
          await submit.submit({ values: submissionData });
          console.log('Submitted Data:', submissionData);
          closeDialog();
      } catch (error) {
          errorMessage.value = 'Failed to submit data. Please try again.';
          console.error('Submission Error:', error);
      } finally {
      }
    };


    const getModeOfPayment = () => {
      if (getProfileOptions()) {
          const profiles = options.profile[autocompleteValue.value.value];
          const profile = profiles.find((p) => p.name === autocompleteProfileValue.value.value);
          return profile ? profile.modes_of_payment : [];
      }
      return [];
    };

    const getProfileOptions = () => {
      const profile = options.profile[autocompleteValue.value.value];
      return profile ? profile.map((item) => item.name) : [];
    };

    const openDialog = () => {
      const posprofile = createResource({
          url: 'ant_pos.ant_pos.api.pos_profile.get_pos_profiles_by_company',
          method: 'GET',

          onSuccess(data) {
          if (data && typeof data === 'object') {
              options.company = Object.keys(data);
              options.profile = data;
          }
          },
      });
      posprofile.fetch();
      dialog1.value = true;
    };
    const validate_pos = createResource({
        url: 'ant_pos.ant_pos.api.pos_profile.get_openingshift',
        method: 'GET',
        auto:true,

        onSuccess(data) {
          if (data){
            Object.assign(base, data);         
            dialog1.value=false;
          }else{
            openDialog()
          }
        },
    });
    watch(autocompleteProfileValue, (newVal, oldVal) => {
      if (newVal.value !== oldVal.value) {
          mode_of_payment.value = getModeOfPayment();
      }
    });
</script>