<template>
    <div id="signin-form">
       <section class="hero is-fullheight">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <div class="column is-6 is-offset-3">
                        <h3 class="title has-text-black">Login</h3>
                        <!-- <hr class="signin-hr"> -->
                        <!-- <p class="subtitle has-text-black">Please login into your account.</p> -->

                        <div v-if="error && submitting">
                            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                        </div>
                        <p v-if="success" class="notification is-success">User successfully logged in.</p>

                        <div class="box">
                            <form @submit.prevent="handleSubmit">
                                <div class="field">
                                    <div class="control">
                                        <input ref="email" @focus="clearStatus" @keypress="clearStatus" v-model="user.email" class="input is-large" type="email" placeholder="Your Email" autofocus="">
                                    </div>
                                </div>

                                <div class="field">
                                    <div class="control">
                                        <input ref="password" @focus="clearStatus" @keypress="clearStatus" v-model="user.password" class="input is-large" type="password" placeholder="Your Password">
                                    </div>
                                </div>
                                <!-- <div class="field">
                                    <label class="checkbox">
                                    <input type="checkbox" ref="remember" @focus="clearStatus" @keypress="clearStatus" v-model="user.remember">
                                    Remember me
                                    </label>
                                </div> -->
                                <button class="button is-block is-info is-large is-fullwidth">Login</button>
                            </form>
                        </div>
                        <p class="has-text-grey">
                            <!-- <router-link to="/signup">Sign Up</router-link> &nbsp;·&nbsp; -->
                            <a href="../">Forgot Password</a> &nbsp;·&nbsp;
                        </p>
                    </div>
                </div>
            </div>
        </section> 
    </div>
</template>

<script>
export default {
   name: 'signin-form',
   data() {
       return {
           submitting: false,
           error: false,
           errors: [],
           success: false,
           response: null,
           user: {
               email: null,
               password: null,
           }
       }
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidEmail()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.signin()
        },
        clearStatus() {
            this.error = false
            this.success = false
            this.errors = []
        },
        showError() {
            this.error = true
            this.submitting = true
            this.success = false
        },
        showSuccess() {
            this.error = false
            this.submitting = false
            this.success = true
            this.clearForm()
            // this.$refs.category.focus()
        },
        signin() {
            this.$store.commit('setUserData', this.user.email)
            this.axios.post('login', {'body': this.user})
            .then(response => {
                if (response.data['success']) {
                    this.$store.commit('setJwtToken', response.data['token'])
                    this.showSuccess()
                    this.$emit('isAuthenticated', this.$store.getters.isAuthenticated)
                } else {
                    this.errors.push({'id':1, 'e': response.data['body']})
                    this.showError()
                }
            })
            .catch(error => {
                this.response = error
                this.showError()
            })
        },
        clearForm() {
           this.user = {
               email: null,
               password: null,
               remember: true
           }
        },
        validEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },
        invalidEmail() {
            if (this.user.email === null) {
                this.errors.push({'id':3, 'e':'!Email is Empty.'})
                return true
            } else if (!this.validEmail(this.user.email)) {
                this.errors.push({'id':4, 'e':'!Email is invalid.'})
                return true
            } else {
                return false
            }
        }
    }
}
</script>

<style scoped>
#submit {
    align-self: center
}
form {
    margin-bottom: 2rem;
}
[class*='-message'] {
    font-weight: 500;
}
.error-message {
    color: #d33c40;
}

.success-message {
    color: #32a95d;
}
</style>