import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import VueAxios from 'vue-axios'
import VModal from 'vue-js-modal'
import router from './router'
import 'vue-search-select/dist/VueSearchSelect.css'

Vue.use(VModal)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
