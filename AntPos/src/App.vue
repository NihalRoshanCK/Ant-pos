<template>
  <div>
    <router-view />
    <div v-if="currentComponent">
      <component :is="currentComponent" />
    </div>
  </div>
</template>

<script setup>
  import { ref , inject } from 'vue';

  let base = inject('base');
  const currentComponent = ref(null); 

  const loadComponent = async (componentName) => {
    try {
      const components = {
        OpenShift: () => import('./component/Dialog/Open-Shift.vue'),
      };

      if (components[componentName]) {
        const component = await components[componentName]();
        currentComponent.value = component.default; // Set the loaded component
      } else {
      console.error(`Component "${componentName}" not found.`);
      currentComponent.value = null;
      }
    } catch (error) {
      console.error('Error loading component:', error);
      currentComponent.value = null;
    }
  };
  
  if (!base.Ant_Opening_Shift.name){
    loadComponent('OpenShift');    
  } 
</script>
