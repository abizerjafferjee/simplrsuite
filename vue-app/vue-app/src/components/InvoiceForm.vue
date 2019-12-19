<template>
    <div id="product-form">

        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link to="/invoices">Invoices</router-link></li>
                <li class="is-active">
                    <a aria-current="page">Add Invoice</a>
                </li>
            </ul>
        </nav>

        <div class="notification" v-if="errorNotification">
            <button @click="closeNotification" class="delete"></button>
            {{ errorNotification }}
        </div>

        <div v-if="error && submitting">
            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
        </div>
        <p v-if="success" class="notification is-success">Successfully added the invoice</p>         

        <section>
            <form>
                <div class="card card-content has-background-light">
                    <div class="columns">
                        <div class="column is-two-fifths">
                            <label class="label">Supplier</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="supplier" @focus="clearStatus" @keypress="clearStatus" :options="suppliers" v-model="invoice.supplier" placeholder="select item"></model-select>
                                </div>
                                <router-link class="control" to="/add-supplier"><button class="button is-small is-link">Add Supplier</button></router-link>
                            </div>
                        </div>
                        <div class="column">
                            <label class="label">Invoice No.</label>
                            <input class="input" ref="date" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.invoice" type="text"/>
                        </div>
                        <div class="column">
                            <label class="label">Invoice Date</label>
                            <input class="input" ref="date" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.date" type="date"/>
                        </div>
                        <div class="column">
                            <label class="label">Total Tax</label>
                            <p class="control is-expanded has-icons-left">
                                <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.total_tax" type="number"/>
                                <span class="icon is-small is-left">TZS</span>
                            </p>
                        </div>
                        <div class="column">
                            <label class="label">Total Amount</label>
                            <p class="control is-expanded has-icons-left">
                                <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.total_cost" type="number"/>
                                <span class="icon is-small is-left">TZS</span>
                            </p>                        
                        </div>
                    </div>                       
                </div>

                <div class="card card-content" v-if="invoice.items.length > 0">
                    <div class="level title is-5">
                        <div class="level-item">Product</div>
                        <div class="level-item">Quantity</div>
                        <div class="level-item">Unit Cost</div>
                        <div class="level-item">Tax</div>
                        <div class="level-item">Total Cost</div>
                    </div>
                    <div class="level has-background-light" v-for="(item, index) in invoice.items" v-bind:key="index">

                        <div class="level-item">
                            {{ item.product }}
                        </div>

                        <div class="level-item">
                            {{ item.quantity }}
                        </div>

                        <div class="level-item">
                            {{ item.unit_cost | currency }}
                        </div>

                        <div class="level-item">
                            {{ item.tax |currency }}
                        </div>

                        <div class="level-item">
                            {{ item.total_cost | currency }}
                        </div>
                    </div>
                </div>

                <div class="card card-content has-text-centered" v-else>There are no items in your invoice. Add an item.</div>
            
                <div class="section">
                    <div class="columns">

                        <div class="column is-two-fifths">
                            <label class="label">Product</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="product" @focus="clearStatus" @keypress="clearStatus" :options="products" v-model="item.product" placeholder="select item"></model-select>
                                </div>
                                <router-link to="/add-product"><font-awesome-icon class="icon has-text-link" icon="plus" size="sm" /></router-link>
                            </div>
                        </div>

                        <div class="column">
                            <label class="label">Quantity</label>
                            <p class="control">
                                <input class="input" ref="quantity" @focus="clearStatus" @keypress="clearStatus" v-model="item.quantity" type="number"/>
                            </p>
                        </div>

                        <div class="column">
                            <label class="label">Unit Cost</label>
                            <p class="control has-icons-left">
                                <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="item.unit_cost" type="number"/>
                                <span class="icon is-small is-left">TZS</span>
                            </p>
                        </div>

                        <div class="column">
                            <label class="label">Tax</label>
                            <p class="control has-icons-left">
                                <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="item.tax" type="number"/>
                                <span class="icon is-small is-left">TZS</span>
                            </p>
                        </div>

                        <div class="column">
                            <label class="label">Total Cost</label>
                            <p class="control has-icons-left">
                                <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="item.total_cost" type="number"/>
                                <span class="icon is-small is-left">TZS</span>
                            </p>
                        </div>
                    </div>
                    
                    <div class="button is-small is-link" @click="addItem()">Add Item</div>
                </div>

                <div class="card card-content has-background-light">
                    <div class="columns">
                        <div class="column is-one-fifth">
                            <label class="label">Invoice Paid?</label>
                            <model-select class="input" ref="paid" @focus="clearStatus" @keypress="clearStatus" :options="booleanOptions" v-model="invoice.paid" placeholder="select item"></model-select>
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.paid">
                            <label class="label">Payment Date</label>
                            <input class="input" ref="date" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.payment.date" type="date"/>
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.paid">
                            <label class="label">Receipt Number</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.payment.receipt" type="number"/>                    
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.paid">
                            <label class="label">Method of Payment</label>
                            <model-select class="input" ref="payment_type" @focus="clearStatus" @keypress="clearStatus" :options="paymentTypes" v-model="invoice.payment.payment_type" placeholder="select item"></model-select>
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.paid && invoice.payment.payment_type === 'CHEQUE'">
                            <label class="label">Cheque No.</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.payment.cheque" type="text"/>
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.paid && invoice.payment.payment_type === 'BANK'">
                            <label class="label">Bank Transfer Ref.</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.payment.bank_transfer" type="text"/>
                        </div>
                        <div class="column is-one-fifth" v-if="!invoice.paid">
                            <label class="label">Payment Terms</label>
                            <model-select class="input" ref="terms" @focus="clearStatus" @keypress="clearStatus" :options="paymentTerms" v-model="invoice.terms" placeholder="select item"></model-select>
                        </div>
                    </div>

                    <div class="columns">
                        <div class="column is-one-fifth">
                            <label class="label">Goods Received?</label>
                            <model-select class="input" ref="received" @focus="clearStatus" @keypress="clearStatus" :options="booleanOptions" v-model="invoice.received" placeholder="select item"></model-select>
                        </div>
                        <div class="column is-one-fifth" v-if="invoice.received">
                            <label class="label">Delivery Number</label>
                            <input class="input" ref="receipt" @focus="clearStatus" @keypress="clearStatus" v-model="invoice.delivery" type="text"/>  
                        </div>
                    </div>

                    <button id="submit" class="button is-primary" @click="handleSubmit()">Submit Invoice</button>
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
    name: 'procurement-form',
    components: {
        ModelSelect
    },
    data() {
        return {
            jwt: '',
            error: false,
            errors: [],
            errorNotification: null,
            submitting: false,
            success: false,
            response: null,
            products: [],
            suppliers: [],
            item:{},
            booleanOptions:[
                {'text': 'True', value: true},
                {'text': 'False', value: false}
            ],
            paymentTypes:[
                {'text': 'Cheque', value: 'CHEQUE'},
                {'text': 'Bank Transfer', value: 'BANK'},
                {'text': 'Cash', value: 'CASH'}
            ],
            paymentTerms:[
                {'text': '30 days', value: '30'},
                {'text': '60 days', value: '60'},
                {'text': '90 days', value: '90'}
            ],
            invoice: {
                supplier: null,
                invoice: null,
                date: null,
                currency: "TZS",
                total_tax: null,
                total_cost: null,
                paid: false,
                terms: null,
                received: false,
                delivery: null,
                items: [],
                payment: {
                    currency: "TZS",
                    payment_date: null,
                    receipt: null,
                    payment_type: null,
                    cheque: null,
                    bank_transfer: null,
                }        
            },
        }
    },
    filters: {
        currency: function (value) {
            return numeral(value).format("0,0")
        },
        date: function (value) {
            return moment(String(value)).format('L')
        }
    },
    created: function() {
        this.jwt = this.$store.state.jwt
        this.getProducts()
        this.getSuppliers()
    },
    methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidSupplier()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addInvoice()
 
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addInvoice() {
            this.axios.post('invoice', {'body': this.invoice}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.showSuccess()
            })
            .catch(e => {
                this.response = e
                this.showError()
            })
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
            // this.$refs.supplier.focus()
        },
        clearForm() {
            this.procurement = {
                supplier: null,
                product: null,
                location: null,
                invoice: null,
                quantity: 0,
                currency: "TZS",
                unit_cost: 0,
                total_cost: 0,
                paid: true,
                additional_info: null
            }
        },
        getProducts() {
            this.axios.get('products/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.products = response.data['products']
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
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
        invalidSupplier() {
            if (this.invoice.supplier === null) {
                this.errors.push({'id':2, 'e':'!Supplier Name is required.'})
                return true
            }
        },
        addItem() {
            this.invoice.items.push(this.item)
            this.item = {}
        }
    }
}
</script>

<style scoped>
/* * {
    font-family: 'Open Sans'
} */
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