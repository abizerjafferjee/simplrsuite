import Vue from 'vue'
import Vuex from 'vuex'

import { isValidJwt, EventBus } from '../utils'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        user: '',
        jwt: ''
    },
    mutations: {  
        setUserData (state, payload) {
          state.user = payload
        },
        setJwtToken (state, payload) {
          localStorage.token = payload
          state.jwt = payload
        }
    },
    getters: {
      isAuthenticated (state) {
        return isValidJwt(state.jwt)
      }
    }
})

