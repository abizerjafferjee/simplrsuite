<template>
    <div id="mail-form">

        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div class="title is-6 has-text-success" v-if="success">{{ success }}</div>
            <div v-else></div>
        </div>

        <div class="card">
            <div class="card-header card-header-title has-background-info has-text-white">Add a Contact</div>
            <form class="card-content" @submit.prevent="handleSubmit">
                <div class="columns is-paddingless">
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
                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">Remarks/ Comments</label>
                        <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="contact.remark"></textarea></div>
                    </div>
                </div>
                
                <button id="submit" class="button is-primary">Add Contact</button>
            </form>
        </div>
        <br>
        <article class="card has-text-centered">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column">Name</div>
                    <div class="column">Organization</div>
                    <div class="column">Email</div>
                    <div class="column">Phone Number</div>
                    <div class="column">Remarks</div>
                </div>
            </div>
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="maillist && maillist.length===0">No contacts in your maillist. Add a contact using the form above.</div>
                <div class="card is-paddingless" v-for="contact in maillist" v-bind:key="contact.id" v-else-if="maillist && maillist.length > 0">
                    <div class="level">
                        <div class="column"><div class="title is-6">{{ contact.name }}</div></div>
                        <div class="column"><div class="title is-6 has-text-info">{{ contact.business }}</div></div>
                        <div class="column"><div class="title is-6">{{ contact.email }}</div></div>
                        <div class="column"><div class="title is-6">{{ contact.phone }}</div></div>
                        <div class="column"><div class="title is-6">{{ contact.remark }}</div></div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getMaillist(pages.page-1)">Previous</a>
                    <a class="pagination-next" :disabled="pages.next==false" @click="getMaillist(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>

    </div>
</template>

<script>
export default {
   name: 'mail-form',
   data() {
       return {
           jwt: '',
           response: null,
           error: null,
           success: null,
           contact: {
               name: null,
               business: null,
               email: null,
               phone: null,
               phone_code: "+255",
               remark: null
           },
           maillist: null,
           pages: {
               page: null,
               next: null,
               prev: null
           },
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getMaillist(1)
   },
   methods: {
        handleSubmit() {
            this.clearStatus()
            this.addContact()
        },
        clearStatus() {
            this.error = null
            this.success = null
        },
        addContact() {
            this.axios.post('maillist', {'body': this.contact}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Contact added."
                this.clearForm()
                this.getMaillist(1)
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status == 400) {
                    this.error = "Error in submitting form."
                } else {
                    this.error = "Internal Server Error."
                }
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
                } else if (error.response.status == 400) {
                    this.error = "Error in retrieving contacts."
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
    }
  
}
</script>

<style scoped>

</style>