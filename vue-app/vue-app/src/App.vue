<template>
  <div id="app" class="container is-fullhd">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
          <img src="./assets/logo_2.jpg" width="150" height="150">
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a v-if="!isAuthenticated" @click="show('signin')" class="button is-light">
              Log in
            </a>
            <a v-if="!isAuthenticated" @click="show('signup')" class="button is-primary">
              <strong>Sign Up</strong>
            </a>
            <a v-if="isAuthenticated && user" class="button is-light">{{ user.name }}</a>
            <a v-if="isAuthenticated" @click="logout()" class="button is-danger is-light">
              Logout
            </a>
          </div>
        </div>
      </div>
    </nav>

    <div class="columns" v-if="isAuthenticated">
      <div class="column is-one-fifth">
        <aside class="menu is-size-5">
          <ul class="menu-list">
            <li><router-link to="/dashboard"><font-awesome-icon class="icon has-text-info font-margin" icon="chart-line" size="lg" />Dashboard</router-link></li>
            <li><router-link to="/add-contact"><font-awesome-icon class="font-margin" icon="at" size="lg" />Mailing List</router-link></li>
          </ul>
          <p class="menu-label">
            Procurement
          </p>
          <ul class="menu-list">
            <li><router-link to="/products"><font-awesome-icon class="icon has-text-info font-margin" icon="store" size="lg" />Products</router-link></li>
            <li><router-link to="/suppliers"><font-awesome-icon class="icon has-text-danger font-margin" icon="truck" size="lg" />Suppliers</router-link></li>
            <li><router-link to="/inventory"><font-awesome-icon class="font-margin" icon="warehouse" size="lg" />Inventory</router-link></li>
            <li><router-link to="/payments"><font-awesome-icon class="icon has-text-success font-margin" icon="money-check-alt" size="lg" />Payments</router-link></li>
          </ul>
        </aside>
      </div>

      <div class="column is-size-5">
        <router-view></router-view>
      </div>
    </div>

    <div class="columns" v-if="!isAuthenticated">
      <div class="column">
        <signin-form v-if="this.signin" @isAuthenticated="authenticate"></signin-form>
        <signup-form v-if="this.signup"></signup-form>
      </div>
    </div>

  </div>
</template>

<script>
import SignUpForm from './components/SignUpForm.vue'
import SignInForm from './components/SignInForm.vue'
export default {
  name: 'app',
  components: {
    'signup-form': SignUpForm,
    'signin-form': SignInForm
  },
  data() {
    return {
      isAuthenticated: false,
      user: null,
      signin: false,
      signup: false,
      response: null
    }
  },
  created () {
    this.authenticate(this.$store.getters.isAuthenticated)
  },
  methods: {
    show(form) {
      if (form === 'signup') {
        this.signup = true
        this.signin = false
      } else {
        this.signup = false
        this.signin = true
      }
    },
    authenticate(isAuthenticated) {
      try {
        if (isAuthenticated) {
          var jwt = this.$store.state.jwt
          this.axios.get('http://localhost:5000/profile', { headers: { Authorization: `Bearer: ${jwt}`}})
          .then(response => {
            this.isAuthenticated = true
            this.user = response.data[0]['user']
            this.$store.commit('setUserData', this.user.email)
            this.signin = false
            this.signup = false
            if (this.$route.path === '/' | this.$route.path === '/signin' | this.$route.path === '/signup') {
              this.$router.push({path: '/dashboard'})
            }
          })
          .catch(e => {
            this.response = e
          })
        } else {
          this.isAuthenticated = false
          this.signin = true
        }
      } catch (error) {
          this.response = error
      }
    },
    logout() {
      this.$store.commit('setUserData', '')
      this.$store.commit('setJwtToken', '')
      this.isAuthenticated = false
      this.user = null
      this.signin = true
    }
  }
}
</script>

<style>
@import "~bulma/css/bulma.css";
#app {
  min-width: 75%;
}
.font-margin {
    margin: 0px 5px 0px 0px;
}
</style>
