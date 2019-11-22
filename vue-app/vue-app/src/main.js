import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import VueAxios from 'vue-axios'
import VModal from 'vue-js-modal'
import router from './router'
import store from './store';
import 'vue-search-select/dist/VueSearchSelect.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const API_URL = process.env.VUE_APP_ROOT_API

library.add(fas)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VModal)
Vue.use(VueAxios, axios)

Vue.axios.defaults.baseURL = API_URL;
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
