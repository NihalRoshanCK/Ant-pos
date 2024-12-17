<template>
    <Dialog :options="{ size: 'lg' }" v-model="dialogVisible" @close="handleDialogClose">
      <template #body-title>
        <h3>Create Item</h3>
      </template>
  
      <template #body-content>
        <div class="grid grid-cols-1 gap-5 w-full place-items-stretch">
          <!-- Item Name -->
          <FormControl
            type="text"
            label="Item Name"
            v-model="item.name"
            placeholder="Enter Item Name"
            size="sm"
          />
  
          <!-- Batch No -->
          <FormControl
            type="text"
            label="Batch No"
            v-model="item.batch_no"
            placeholder="Enter Batch No"
            size="sm"
          />
  
          <!-- Serial No -->
          <FormControl
            type="text"
            label="Serial No"
            v-model="item.serial_no"
            placeholder="Enter Serial No"
            size="sm"
          />
        </div>
      </template>
  
      <template #actions>
        <Button variant="solid" @click="createItem">Submit</Button>
        <Button class="ml-2" @click="handleDialogClose">Close</Button>
      </template>
    </Dialog>
  </template>


<script setup>
import { Dialog, createListResource, Button, FormControl, createResource } from 'frappe-ui';

console.log("heyyyyyyyy.......");

</script>