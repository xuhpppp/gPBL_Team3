import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAddressCard, faComputer } from '@fortawesome/free-solid-svg-icons'

library.add(faAddressCard)
library.add(faComputer)

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(router).mount('#app')
