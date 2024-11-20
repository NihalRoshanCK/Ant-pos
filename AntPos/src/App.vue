<template>
  <div>
    <router-view />
    <Dialog v-model="dialog1">
      <template #body-title>
        <h3>Create ANT Opening Shift</h3>
      </template>
      <template #body-content>
        <div class="flex flex-col gap-8">
          <div class="">
            <FormControl
              type="autocomplete"
              :options="[
                {
                  label: 'One',
                  value: '1',
                },
                {
                  label: 'Two',
                  value: '2',
                },
                {
                  label: 'Three',
                  value: '3',
                },
              ]"
              size="sm"
              variant="subtle"
              placeholder="Placeholder"
              :disabled="false"
              label="Company"
              v-model="autocompleteValue"
              hide-search="true"
            />
          </div>
          <div>
            <FormControl
              type="autocomplete"
              :options="[
                {
                  label: 'One',
                  value: '1',
                },
                {
                  label: 'Two',
                  value: '2',
                },
                {
                  label: 'Three',
                  value: '3',
                },
              ]"
              size="sm"
              variant="subtle"
              placeholder="Placeholder"
              :disabled="false"
              label="Company"
              v-model="autocompleteValue"
              hide-search="true"
            />

          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="solid" @click="confirmShift">Confirm</Button>
        <Button class="ml-2" @click="closeDialog">Close</Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { createResource, Button, Dialog, Autocomplete,FormControl  } from 'frappe-ui';
import { inject, ref } from 'vue';
const single= ref('')
const dialog1 = ref(false); // Reactive variable for dialog state
const base = inject('base');

// Function to close the dialog
const closeDialog = () => {
  dialog1.value = false; // Update reactive property
};

// Function to handle confirmation action
const confirmShift = () => {
  console.log('Opening shift confirmed.');
  closeDialog(); // Close the dialog after confirmation
};

// Create a resource to fetch data
let post = createResource({
  url: 'ant_pos.ant_pos.api.pos-profile.get_openingshift',
  method: 'GET',
  auto: true,
  onSuccess(data) {
    if (!data || !data.Ant_Opening_Shift) {
      dialog1.value = true; // Show dialog if no opening shift data
    }
    Object.assign(base, data); // Merge fetched data into `base`
  },
});
</script>
