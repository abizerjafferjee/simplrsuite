<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/payments">Payments</router-link></li>
                    <li class="is-active">
                        <a aria-current="page">Record Payment</a>
                    </li>
                </ul>
                </nav>

                <section class="hero welcome is-small has-background-light">
                    <div class="hero-body">
                        <div class="container">
                            <p class="title">Record Payment</p>
                            <p class="subtitle">Select the invoices you want to record payment for and keep your outstanding amounts in check</p>
                        </div>
                    </div>
                </section>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>

                <section>
                    <div class="content">
                        <div v-if="error && submitting">
                            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                        </div>
                        <p v-if="success" class="notification is-success">Payment recorded successfully.</p>

                        <form @submit.prevent="handleSubmit">

                            <label class="label">* Supplier</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="supplier" @focus="clearStatus" @keypress="clearStatus" :options="supplierNames" v-model="payment.supplier_id" placeholder="select item"></model-select>
                                </div>
                                <div class="control"><router-link to="/add-supplier" class="button">Add Supplier</router-link></div>
                            </div>

                            <label class="label">Total Amount</label>
                            <div class="field has-addons">
                                <p class="control">
                                    <span class="select">
                                    <select class="button is-light" ref="currency" @focus="clearStatus" @keypress="clearStatus" v-model="payment.currency" type="text">
                                        <option>TZS</option>
                                        <option>KES</option>
                                        <option>USD</option>
                                        <option>RMB</option>
                                        <option>AED</option>
                                    </select>
                                    </span>
                                </p>
                                <p class="control is-expanded">
                                    <input ref="amount" @focus="clearStatus" @keypress="clearStatus" v-model="payment.amount" class="input" type="number" placeholder=5000>
                                </p>
                            </div>

                            <label class="label">Invoices</label>
                            <p v-if="payment.supplier_id === null">Select a supplier to show outstanding invoices</p>
                            <table class="table" v-else>
                                <tbody>
                                    <tr v-for="(invoice, index) in outStandingInvoices" v-bind:key="index">
                                        <td>{{ invoice.invoice }}</td>
                                        <td>{{ invoice.total_cost }}</td>
                                        <td>{{ invoice.created }}</td>
                                        <td><input :id="invoice.invoice" :value="invoice.invoice" name="invoice" type="checkbox" v-model="payment.invoices" /></td>
                                    </tr>
                                </tbody>
                            </table>

                            <p v-if="payment_caution_flag" class="error-message">!Caution: Total sum of invoices does not match total amount.
                                If you submit the unmatched amount, selected invoices will still be recorded as paid.</p>

                            <label class="label">Additional Info</label>
                            <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="payment.additional_info" placeholder="e.g. Product description, dimensions, weight and colors."></textarea></div>
                            
                            <button id="submit" class="button is-primary">Record Payment</button>
                        </form>
                    </div>
                </section>
            </article>
        </div>

    </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select'

export default {
   name: 'payments-form',
    components: {
        ModelSelect
    },
   data() {
       return {
           submitting: false,
           error: false,
           success: false,
           response: null,
           errors: [],
           errorNotification: null,
           payment_caution_flag: false,
           payment: {
               supplier_id: null,
               amount: 0,
               invoices: [],
               currency: "TZS",
               additional_info: null,
           },
           supplierNames: [],
           outStandingInvoices: [],
           jwt: ''
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getSupplierNames()
   },
   watch: {
       'payment.supplier_id': function() {
           this.getOutStandingInvoices()
       },
       'payment.amount': function() {
           if (this.payment.invoices.length > 0) {
               this.invalidAmount()
           }    
       },
       'payment.invoices': function() {
           this.invalidAmount()
       }
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidSupplier()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.recordPayment()
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
        recordPayment() { 
            try {
                this.axios.post('payments', {'body': this.payment, 'from': 'form'}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.showSuccess()
                    }
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
        clearForm() {
           this.payment = {
               supplier_id: null,
               amount: 0,
               invoices: [],
               currency: "TZS",
               additional_info: null,
           }
        },
        getSupplierNames() {
            try {
                this.axios.get('suppliers/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.supplierNames = response.data[0]['suppliers']
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
        getOutStandingInvoices(){
            try {
                this.axios.get('payments/due/' + this.payment.supplier_id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.outStandingInvoices = response.data[0]['body']
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
        invalidSupplier() {
            if (this.payment.supplier_id === null) {
                this.errors.push({'id':1, 'e':'Please select a supplier.'})
                return true
            }
            return false
        },
        invalidAmount() {
           var sum = 0
           for (var i=0; i < this.outStandingInvoices.length; i++) {
               if (this.payment.invoices.includes(this.outStandingInvoices[i]['invoice'])) {
                   sum += this.outStandingInvoices[i]['total_cost']
               }
           }

           if (sum !== Number(this.payment.amount)) {
               this.payment_caution_flag = true
           } else {
               this.payment_caution_flag = false
           }
        },
        closeNotification() {
            this.errorNotification = null
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