<template>
  <div>
    <router-view />
    <Dialogs />
  </div>
</template>

<script setup>
import { Dialogs } from './utils/ErrorDialog'
</script>
