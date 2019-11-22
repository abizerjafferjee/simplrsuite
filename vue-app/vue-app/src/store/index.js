import Vue from 'vue'
import Vuex from 'vuex'

import { isValidJwt } from '../utils'

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
          localStorage.jwt = payload
          state.jwt = payload
        }
    },
    getters: {
      isAuthenticated (state) {
        if (isValidJwt(state.jwt)) {
          return true
        } else {
          var jwt = localStorage.jwt
          state.jwt = jwt
          if (isValidJwt(state.jwt)) {
            return true
          }
        }
        return false
      }
    }
})

