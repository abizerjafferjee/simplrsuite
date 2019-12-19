<template>
    <div id="product-form">

        <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
            <li><router-link to="/payments">Payments</router-link></li>
            <li class="is-active">
                <a aria-current="page">Record Payment</a>
            </li>
        </ul>
        </nav>

        <div class="notification" v-if="errorNotification">
            <button @click="closeNotification" class="delete"></button>
            {{ errorNotification }}
        </div>         

        <section>
            <form @submit.prevent="handleSubmit">
                <div class="card card-content has-background-light">
                    <div class="columns">
                        <div class="column is-three-fifths">
                            <label class="label">Supplier</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="supplier" @focus="clearStatus" @keypress="clearStatus" :options="suppliers" v-model="payment.supplier_id" placeholder="select item"></model-select>
                                </div>
                                <div class="control"><router-link to="/add-supplier" class="button">Add Supplier</router-link></div>
                            </div>
                        </div>
                        <div class="column">
                            <label class="label">Payment Date</label>
                            <input class="input" ref="date" @focus="clearStatus" @keypress="clearStatus" v-model="payment.date" type="date"/>
                        </div>
                        <div class="column">
                            <label class="label">Receipt Number</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="payment.receipt" type="text"/>
                        </div>
                    </div>                       

                    <label class="label">Click the checkbox next to the invoices that you want to include in your payment record.</label>
                    <p v-if="payment.supplier_id === null">Select a supplier to show outstanding invoices</p>
                    <p v-if="invoices.length === 0 && payment.supplier_id">This supplier has 0 outstanding invoices.</p>

                    <table class="table" v-if="invoices.length > 0 && payment.supplier_id">
                        <thead>
                            <td>Invoice Number</td>
                            <td>Amount</td>
                            <td>Date</td>
                            <td></td>
                        </thead>
                        <tbody>
                            <tr v-for="(invoice, index) in invoices" v-bind:key="index">
                                <td>{{ invoice.invoice_number }}</td>
                                <td>{{ invoice.currency }} {{ invoice.total_cost | currency }}</td>
                                <td>{{ invoice.date }}</td>
                                <td><input :id="invoice.id" :value="invoice.id" name="invoice" type="checkbox" v-model="payment.invoices" /></td>
                            </tr>
                        </tbody>
                    </table>

                    <div class="columns">
                        <div class="column is-one-fifth">
                            <label class="label">Method of Payment</label>
                            <model-select class="input" ref="payment_type" @focus="clearStatus" @keypress="clearStatus" :options="paymentTypes" v-model="payment.payment_type" placeholder="select item"></model-select>
                        </div>
                        <div class="column is-one-fifth" v-if="payment.payment_type === 'CHEQUE'">
                            <label class="label">Cheque No.</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="payment.cheque" type="text"/>
                        </div>
                        <div class="column is-one-fifth" v-if="payment.payment_type === 'BANK'">
                            <label class="label">Bank Transfer Ref.</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="payment.bank_transfer" type="text"/>
                        </div>
                    </div>

                    <button id="submit" class="button is-primary">Record Payment</button>
    
                </div>

            </form>
        </section>

    </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select'
var numeral = require("numeral");
import moment from 'moment'

export default {
   name: 'payments-form',
    components: {
        ModelSelect
    },
   data() {
       return {
           jwt: '',
           submitting: false,
           error: false,
           success: false,
           response: null,
           errors: [],
           errorNotification: null,
           paymentTypes:[
                {'text': 'Cheque', value: 'CHEQUE'},
                {'text': 'Bank Transfer', value: 'BANK'},
                {'text': 'Cash', value: 'CASH'}
           ],
           payment: {
               supplier_id: null,
               invoices: [],
               payment_type: null,
               receipt: null,
               cheque: null,
               bank_transfer: null,
               date: null,
               reason: null,
           },
           suppliers: [],
           invoices: [],
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getSuppliers()
   },
   watch: {
       'payment.supplier_id': function() {
           if (this.payment.supplier_id) {
               this.getInvoices()
           }
       },
   },
    filters: {
        currency: function (value) {
            return numeral(value).format("0,0")
        },
        date: function (value) {
            return moment(String(value)).format('L')
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
            this.axios.post('payment', {'body': this.payment}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
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
        },
        clearForm() {
           this.payment = {
               supplier_id: null,
               invoices: [],
               payment_type: null,
               receipt: null,
               cheque: null,
               bank_transfer: null,
               date: null,
               reason: null,
           }
        },
        getSuppliers() {
            this.axios.get('suppliers/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.suppliers = response.data['suppliers']
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        getInvoices(){
            this.axios.get('invoices/' + this.payment.supplier_id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.invoices = response.data['body']
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        invalidSupplier() {
            if (this.payment.supplier_id === null) {
                this.errors.push({'id':1, 'e':'Please select a supplier.'})
                return true
            }
            return false
        },
        closeNotification() {
            this.errorNotification = null
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