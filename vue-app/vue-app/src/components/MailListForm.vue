<template>
    <div id="mail-form">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero welcome is-small has-background-light">
                    <div class="hero-body">
                        <div class="container">
                            <p class="title">Add to Mailing List</p>
                            <p class="subtitle">Add your contact information.</p>
                        </div>
                    </div>
                </section>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>

                <div class="content">
                    <form @submit.prevent="handleSubmit">
                        
                        <label class="label">Full Name</label>
                        <input  class="input" ref="name" @focus="clearStatus" @keypress="clearStatus" v-model="mailer.name" type="text"/>

                        <label class="label">Business/ Organization</label>
                        <input class="input" ref="business" @focus="clearStatus" @keypress="clearStatus" v-model="mailer.business" type="text" placeholder="e.g. Thumbtack"/>

                        <label class="label">Email</label>
                        <input class="input" ref="email" @focus="clearStatus" @keypress="clearStatus" v-model="mailer.email" type="text" />
                        
                        <label class="label">Phone Number</label>
                        <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field is-expanded">
                            <div class="field has-addons">
                                <p class="control"><a class="button is-static">+255</a></p>
                                <p class="control is-expanded">
                                <input ref="phone" @focus="clearStatus" @keypress="clearStatus" v-model="mailer.phone" class="input" type="tel" placeholder="Do not enter the first zero.">
                                </p>
                            </div>
                            </div>
                        </div>
                        </div>

                        <label class="label">Remark/ Comment</label>
                        <textarea class="textarea" ref="remark" @focus="clearStatus" @keypress="clearStatus" v-model="mailer.remark"></textarea>

                        <p v-if="error && submitting" class="error-message">!Please fill out all required fields</p>
                        <p v-if="success" class="success-message">Product successfully added</p>
                        
                        <button id="submit" class="button is-primary">Add Contact</button>
                    </form>
                </div>
            </article>
        </div>
    </div>
</template>

<script>
export default {
   name: 'mail-form',
   data() {
       return {
           submitting: false,
           error: false,
           errorNotification: null,
           success: false,
           mailer: {
               name: null,
               business: null,
               email: null,
               phone: null,
               remark: null
           },
           mailers: [],
           response: null
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
    //    this.getCategories()
   },
   computed: {
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            this.clearStatus()
            this.addMailer(this.mailer)
            this.error = false
            this.success = true
            this.submitting = false
            this.$refs.category.focus()
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addMailer(mailer) {
            try {
                this.axios.post('http://localhost:5000/mailer/add', {'body': mailer}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        var newMailer = response.data[0]['mailer']
                        this.mailers.push(newMailer)
                    }
                })
                .catch(e => {
                    this.response = e
                    this.errorNotification = "Internal Server Error."
                })
            } catch (error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
        },
        closeNotification() {
            this.errorNotification = null
        }
    }
  
}
</script>

<style scoped>

</style>