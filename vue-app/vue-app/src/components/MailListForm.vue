<template>
    <div id="mail-form">

        <div class="section notification" v-if="error">
            <button @click="closeNotification" class="delete"></button>
            {{ error }}
        </div>

        <div v-if="error && submitting">
            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
        </div>
        <p v-if="success" class="notification is-success">Contact successfully added</p>

        <div class="section">
            <div class="card card-content has-background-light">
                <form @submit.prevent="handleSubmit">
                    <div class="columns">
                        <div class="column">
                            <label class="label">* Full Name</label>
                            <input class="input" ref="name" @focus="clearStatus" @keypress="clearStatus" v-model="contact.name" type="text"/>
                        </div>

                        <div class="column">
                            <label class="label">Business/ Organization</label>
                            <input class="input" ref="business" @focus="clearStatus" @keypress="clearStatus" v-model="contact.business" type="text" placeholder="e.g. Thumbtack"/>
                        </div>

                        <div class="column">
                            <label class="label">* Email</label>
                            <div class="field">
                                <div class="control">
                                    <input ref="email" @focus="clearStatus" @keypress="clearStatus" v-model="contact.email" class="input" type="email" placeholder="e.g. alexsmith@gmail.com">
                                </div>
                            </div>
                        </div>
                        
                        <div class="column">
                            <label class="label">* Phone Number</label>
                            <div class="field has-addons">
                            <p class="control">
                                <span class="select">
                                <select class="button is-light" ref="phone_code" @focus="clearStatus" @keypress="clearStatus" v-model="contact.phone_code" type="text">
                                    <option>+255</option>
                                    <option>+254</option>
                                    <option>+86</option>
                                    <option>+971</option>
                                    <option>+1</option>
                                </select>
                                </span>
                            </p>
                            <p class="control is-expanded">
                                <input ref="phone" @focus="clearStatus" @keypress="clearStatus" v-model="contact.phone" class="input" type="tel" placeholder="Do not enter the first zero.">
                            </p>
                            </div>
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column">
                            <label class="label">Remarks/ Comments</label>
                            <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="contact.remark"></textarea></div>
                        </div>
                    </div>
                    
                    <button id="submit" class="button is-primary">Add Contact</button>
                </form>
            </div>
        </div>

        <div class="section">
            <div class="card card-table" v-if="maillist">
                <table class="table is-fullwidth is-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Business/ Organization</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Remarks</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="contact in maillist" v-bind:key="contact.id">
                            <td>{{ contact.name }}
                            <td>{{ contact.business }}</td>
                            <td>{{ contact.email }}</td>
                            <td>{{ contact.phone }}
                            <td>{{ contact.remark }}</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td><a class="pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getMaillist(pages.page-1)">Previous</a></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td><a class="pagination-next" :disabled="pages.next==false" @click="getMaillist(pages.page+1)">Next page</a></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="notification" v-else>
                <div class="title has-text-grey has-text-centered">No contacts in your maillist.</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
   name: 'mail-form',
   data() {
       return {
           submitting: false,
           errors: [],
           error: null,
           success: false,
           contact: {
               name: null,
               business: null,
               email: null,
               phone: null,
               phone_code: "+255",
               remark: null
           },
           maillist: [],
           pages: {
               page: null,
               next: null,
               prev: null
           },
           response: null,
           jwt: '',
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getMaillist(1)
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidName() || this.invalidPhone() || this.invalidEmail()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addContact()
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
        },
        addContact() {
            this.axios.post('maillist', {'body': this.contact}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.showSuccess()
                this.getMaillist(1)
            })
            .catch(e => {
                this.response = e
                this.showError()
            })
        },
        getMaillist(page) {
            this.axios.get('maillist?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.maillist = response.data.body
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        clearForm() {
           this.contact = {
               name: null,
               business: null,
               email: null,
               phone_code: "+255",
               phone: null,
               remark: null
           }
        },
        validEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },
        validPhone(phone) {
            var re = /^\+?\d{9}$/;
            return re.test(phone);
        },
        invalidName() {
           if (this.contact.name === null) {
               this.errors.push({'id':1, 'e':'!Name is Empty.'})
               return true
           } else {
               return false
           }
        },
        invalidPhone() {
            if (this.contact.phone === null) {
                this.errors.push({'id':2, 'e':'!Phone Number is Empty.'})
                return true
            } else if (!this.validPhone(this.contact.phone)) {
                this.errors.push({'id': 5, 'e':'!Phone Number should be 9 digits.'})
                return true
            } else {
                return false
            }
        },
        invalidEmail() {
            if (this.contact.email === null) {
                this.errors.push({'id':3, 'e':'!Email is Empty.'})
                return true
            } else if (!this.validEmail(this.contact.email)) {
                this.errors.push({'id':4, 'e':'!Email is invalid.'})
                return true
            } else {
                return false
            }
        },
        closeNotification() {
            this.error = null
        }
    }
  
}
</script>

<style scoped>

</style>