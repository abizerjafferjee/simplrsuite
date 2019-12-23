<template>
    <div id="supplier-form">

        <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
            <li><router-link to="/suppliers">Suppliers</router-link></li>
            <li class="is-active">
                <a aria-current="page">Add Supplier</a>
            </li>
        </ul>
        </nav>

        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div class="title is-6 has-text-success" v-if="success">{{ success }}</div>
            <div v-else></div>         
        </div>


        <article class="card">
            <div class="card-header card-header-title has-background-info has-text-white">Add a Supplier</div>
            <form class="card-content" @submit.prevent="handleSubmit">
                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">* Supplier Name</label>
                        <input class="input" ref="business_name" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.business_name" type="text" placeholder="e.g. thumbtack"/>
                    </div>
                    <div class="column">
                        <label class="label">Contact Name</label>
                        <input class="input" ref="contact_name" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.contact_person" type="text" placeholder="e.g. John Doe"/>
                    </div>
                </div>

                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">* Email</label>
                        <div class="field">
                            <div class="control">
                                <input ref="email" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.email" class="input" type="email" placeholder="e.g. alexsmith@gmail.com">
                            </div>
                        </div>
                    </div>
                    <div class="column">
                        <label class="label">* Phone Number</label>
                        <div class="field has-addons">
                        <p class="control">
                            <span class="select">
                            <select class="button is-light" ref="phone_code" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.phone_code" type="text">
                                <option>+255</option>
                                <option>+254</option>
                                <option>+86</option>
                                <option>+971</option>
                                <option>+1</option>
                            </select>
                            </span>
                        </p>
                        <p class="control is-expanded">
                            <input ref="phone" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.phone" class="input" type="tel" placeholder="Do not enter the first zero.">
                        </p>
                        </div>
                    </div>
                </div>

                <div class="columns is-paddingless">
                    <div class="column is-two-fifths">
                        <label class="label">Simplr Post Address Link</label>
                        <div class="field">
                            <div class="control">
                                <input ref="plus_code" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.plus_code" class="input" type="text" placeholder="">
                            </div>
                        </div>
                    </div>

                    <div class="column">
                        <label class="label">Address</label>
                        <div class="field">
                            <div class="control">
                                <input ref="address" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.address" class="input" type="text" placeholder="">
                            </div>
                        </div>
                    </div>
                </div>

                <button id="submit" class="button is-primary">Add Supplier</button>
            </form>
        </article>


    </div>
</template>

<script>
export default {
   name: 'supplier-form',
   data() {
       return {
           jwt: '',
           response: null,
           error: null,
           success: null,
           supplier: {
               business_name: null,
               contact_person: null,
               phone: null,
               phone_code: "+255",
               email: null,
               plus_code: null,
               address: null
           },
       }
   },
   created () {
       this.jwt = this.$store.state.jwt
   },
   methods: {
        handleSubmit() {
            this.clearStatus()
            this.addSupplier()
        },
        clearStatus() {
            this.error = null
            this.success = null
        },
        addSupplier() {
            this.axios.post('suppliers', {'body': this.supplier}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Supplier added."
                this.clearForm()
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status == 400) {
                    this.error = error.response.data['message']
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        clearForm() {
           this.supplier = {
               business_name: null,
               contact_person: null,
               phone: null,
               phone_code: "+255",
               email: null,
               plus_code: null,
               address: null
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