<template>
  <div class="w-screen h-screen">
    <div class="w-screen h-[6%]">
      <Navbar/>
    </div>
    <div class="w-screen h-[94%] flex">
      <div class="w-1/2 ">
        <div>
          <div class="p-2">
            <FormControl
              type="text"
              placeholder="Search Items"
            >
              <template #prefix>
                <FeatherIcon
                  class="w-4"
                  name="search"
                />
              </template>
            </FormControl>
          </div>
        </div>
      </div>
      <div class="w-1/2">

      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../component/Navbar.vue'
import {FormControl ,FeatherIcon} from 'frappe-ui'
</script>
