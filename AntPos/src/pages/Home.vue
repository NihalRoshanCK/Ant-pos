  <template>
    <div class="w-screen h-screen">
      <div v-if="currentComponent">
          <component :is="currentComponent" />
      </div>
      <div class="w-screen h-[6%]">
        <Navbar />
      </div>
      <div class="w-screen h-[94%] flex p-2 gap-4">
        <ItemSelector v-if="base.status=='' " />
        <Invoice v-if="base.status=='invoice'"/>
        <ItemDetail/>
      </div>
    </div>
  </template>

  <script setup>
    import Navbar from '../component/Navbar.vue';
    import ItemSelector from '../component/ItemSelector.vue';
    import ItemDetail from '../component/ItemDetail.vue';

    import { FeatherIcon, Autocomplete, createListResource ,Button } from 'frappe-ui';
    import { computed, inject, provide , watch,  } from 'vue';
    import { useDynamicComponent } from '../utils/Dialog';
  import Invoice from '../component/Invoice.vue';

    let base = inject('base');
    const { currentComponent, loadComponent } = useDynamicComponent();
    loadComponent('OpenShift');

    provide('dynamicComponent', { currentComponent, loadComponent });


  </script>

