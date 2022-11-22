import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAddressCard, faCalendarDays, faComputer, faKey, faListCheck, faPowerOff, faUserPlus, faVideo } from '@fortawesome/free-solid-svg-icons'

library.add(faAddressCard,
  faComputer,
  faCalendarDays,
  faListCheck,
  faVideo,
  faUserPlus,
  faPowerOff,
  faKey)

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(router).mount('#app')
