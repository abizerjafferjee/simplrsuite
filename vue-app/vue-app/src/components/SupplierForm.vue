<template>
    <div id="product-form">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/suppliers">Suppliers</router-link></li>
                    <li class="is-active">
                        <a v-if="this.editing" href="#" aria-current="page">Edit Supplier</a>
                        <a href="#" aria-current="page" v-else>Add Supplier</a>
                    </li>
                </ul>
                </nav>

                <p class="title">Add Supplier</p>
                <p class="subtitle">Manage your supplier information. This will be helpful in inventory tracking.</p>
                <div class="content">
                    <div v-if="error && submitting">
                        <p class="error-message" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                    </div>
                    <!-- <p v-if="error && submitting" class="error-message">!Please fill out all fields with an asterisk (*).</p> -->
                    <p v-if="success" class="success-message">Supplier successfully added</p>
                    <form @submit.prevent="handleSubmit">

                        <label class="label">* Supplier Name</label>
                        <input class="input" ref="business_name" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.business_name" type="text" placeholder="e.g. thumbtack"/>

                        <label class="label">Contact Name</label>
                        <input class="input" ref="contact_name" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.contact_person" type="text" placeholder="e.g. John Doe"/>

                        <label class="label">* Phone Number</label>
                        <div class="field is-horizontal">
                            <div class="field-body">
                                <div class="field is-expanded">
                                <div class="field has-addons">
                                    <p class="control"><a class="button is-static">+255</a></p>
                                    <p class="control is-expanded">
                                    <input ref="phone" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.phone" class="input" type="tel" placeholder="Do not enter the first zero.">
                                    </p>
                                </div>
                                </div>
                            </div>
                        </div>

                        <label class="label">* Email</label>
                        <div class="field">
                            <div class="control">
                                <input ref="email" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.email" class="input" type="email" placeholder="e.g. alexsmith@gmail.com">
                            </div>
                        </div>

                        <label class="label">Plus Code</label>
                        <div class="field">
                            <div class="control">
                                <input ref="plus_code" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.plus_code" class="input" type="text" placeholder="">
                            </div>
                        </div>

                        <label class="label">Address</label>
                        <div class="field">
                            <div class="control">
                                <input ref="address" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.address" class="input" type="text" placeholder="">
                            </div>
                        </div>

                        <label class="label">Additional Info</label>
                        <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="supplier.additional_info"></textarea></div>

                        <button id="submit" class="button is-primary" v-if="editing">Save</button>
                        <button id="submit" class="button is-primary" v-else>Add Supplier</button>
                    </form>
                </div>
            </article>
        </div>

    </div>
</template>

<script>
export default {
   name: 'supplier-form',
   props: ['editSupplier'],
   data() {
       return {
           submitting: false,
           error: false,
           errors: [],
           success: false,
           supplier: {
               business_name: null,
               contact_person: null,
               phone: null,
               email: null,
               plus_code: null,
               address: null,
               additional_info: null
           },
           editing: false,
           supplier_id: null,
           response: null
       }
   },
   mounted () {
    //    eslint-disable-next-line
    //    console.log(this.$route.query.editSupplier)
       if (this.$route.query.editSupplier) {
           this.editing = true
           this.supplier_id = this.$route.query.editSupplier
           this.editSupplierForm()
       }
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidSupplier() || this.invalidPhone() || this.invalidEmail()) {
                this.showError()
                return
            }
            this.clearStatus()
            if (this.editing) {
                this.saveSupplier()
            } else {
                this.addSupplier()
            }
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
        addSupplier() {
            try {
                this.axios.post('http://localhost:5000/suppliers', {'body': this.supplier})
                .then(response => {
                    this.response = response
                    this.showSuccess()
                })
                .catch(e => {
                    this.response = e
                    this.showError()
                })
            } catch (error) {
                this.response = error
                this.showError()
            }
        },
        saveSupplier() {
            try {
                this.axios.put('http://localhost:5000/suppliers?id='+this.supplier_id, {'body': this.supplier})
                .then(response => {
                    this.response = response
                    this.showSuccess()
                })
                .catch(e => {
                    this.response = e
                    this.showError()
                })
            } catch (error) {
                this.response = error
                this.showError()
            }
        },
        editSupplierForm() {
            try {
                this.axios.get('http://localhost:5000/suppliers/'+this.supplier_id)
                .then(response => {
                    var body = response.data[0].body
                    this.supplier.business_name = body['business_name']
                    this.supplier.contact_person = body['contact_person']
                    this.supplier.phone = body['phone']
                    this.supplier.email = body['email']
                    this.supplier.plus_code = body['plus_code']
                    this.supplier.address = body['address']
                    this.supplier.additional_info = body['additional_info']
                    // eslint-disable-next-line
                    // console.log(this.supplier)
                })
                .catch(error => {
                    this.response = error
                })
            } catch (error) {
                this.response = error
            }
        },
        clearForm() {
           this.supplier = {
               business_name: null,
               contact_person: null,
               phone: null,
               email: null,
               plus_code: null,
               address: null,
               additional_info: null
           }
        },
        validEmail: function (email) {
            var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },
        validPhone: function (phone) {
            var re = /^\+?\d{9}$/;
            return re.test(phone);
        },
        invalidSupplier() {
           if (this.supplier.business_name === null) {
               this.errors.push({'id':1, 'e':'!Supplier Name is Empty.'})
               return true
           } else {
               return false
           }
        },
        invalidPhone() {
            if (this.supplier.phone === null) {
                this.errors.push({'id':2, 'e':'!Phone Number is Empty.'})
                return true
            } else if (!this.validPhone(this.supplier.phone)) {
                this.errors.push({'id': 5, 'e':'!Phone Number should be 9 digits.'})
                return true
            } else {
                return false
            }
        },
        invalidEmail() {
            if (this.supplier.email === null) {
                this.errors.push({'id':3, 'e':'!Email is Empty.'})
                return true
            } else if (!this.validEmail(this.supplier.email)) {
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