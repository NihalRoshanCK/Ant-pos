import './index.css'

import { createApp, reactive } from 'vue'
import router from './router'
import App from './App.vue'
import mitt from 'mitt';

import {
  Button,
  Card,
  Input,
  setConfig,
  frappeRequest,
  resourcesPlugin,
} from 'frappe-ui'
import Invoice from './component/Invoice.vue';

const app = createApp(App)

// Create event bus
const emitter = mitt();

setConfig('resourceFetcher', frappeRequest)

app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.component('Card', Card)
app.component('Input', Input)

// Create a reactive base object and provide it
const base = reactive({
  Ant_Opening_Shift:{},
  items:[],
  status:'',
  invoice:{},
})
app.provide('base', base) // 'base' is the key for injection

// Provide emitter it globally
app.provide('emitter', emitter);

app.mount('#app')