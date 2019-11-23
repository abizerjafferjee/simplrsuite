<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">
                <div class="content">
                    <section class="hero is-light welcome is-small">
                        <div class="hero-body">
                            <div class="container level">
                                <h1 class="title level-left">
                                    Payments
                                </h1>
                                <div class="level-right">
                                    <p class="level-item"><router-link to="/record-payment" class="button">Record Payment</router-link></p>
                                </div>
                            </div>
                        </div>
                    </section>

                    <div class="notification" v-if="errorNotification">
                        <button @click="closeNotification" class="delete"></button>
                        {{ errorNotification }}
                    </div>         
                    <br>

                    <section class="info-tiles">
                        <div class="tile is-ancestor has-text-centered" v-if="stats">
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">TZS {{ stats.total_outstanding | currency }}</p>
                                    <p class="subtitle">Total Outstanding Amount</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">{{ stats.total_invoices }}</p>
                                    <p class="subtitle">Total Outstanding Invoices</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">TZS {{ stats.uninvoiced_outstanding | currency }}</p>
                                    <p class="subtitle">Total Procurement without Invoices</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title" v-if="stats.latest_payment.created">{{ stats.latest_payment.created | date }}</p>
                                    <p class="title" v-else>No Payments</p>
                                    <p class="subtitle">Last Payment</p>
                                </article>
                            </div>
                        </div>
                    </section>
                    
                    <br>
                    
                    <div class="columns">
                        <div class="column">
                            <div class="card events-card">
                                <header class="card-header">
                                    <p class="card-header-title">
                                        Outstanding Invoices
                                    </p>
                                </header>
                                <div class="card-table" style="height:500px">
                                    <div class="content" v-if="outstandingPayments && outstandingPayments.length > 0">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr>
                                                    <th>Supplier (Id)</th>
                                                    <th>Amount</th>
                                                    <th>Number of Invoices</th>
                                                    <th>Record as Paid</th>
                                                </tr>
                                                <tr v-for="(payment, index) in outstandingPayments" v-bind:key="index">
                                                    <td>{{ payment.business_name }} ({{ payment.supplier_id }})</td>
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td v-if="payment.invoices">{{ payment.invoices.length }} Invoices</td>
                                                    <td><a class="button is-primary" @click="recordInvoicedPayment(index)"><font-awesome-icon class="icon has-text-white" icon="check" size="sm" /></a></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="content is-vcentered notification" v-else>
                                        <p class="is-centered">No outstanding invoice amounts to show</p>
                                    </div>
                                </div>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pagesOutstanding.prev==false" @click="getOutstandingPayments(pagesOutstanding.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="pagesOutstanding.next==false" @click="getOutstandingPayments(pagesOutstanding.page+1)">Next page</a>
                                </footer>
                            </div>
                        </div>

                        <div class="column">
                            <div class="card events-card">
                                <header class="card-header">
                                    <p class="card-header-title">
                                        Payments Made
                                    </p>
                                </header>
                                <div class="card-table" style="height:500px">
                                    <div class="content" v-if="paymentsMade && paymentsMade.length > 0">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr>          
                                                    <th>Payment Id</th>                              
                                                    <th>Supplier (Id)</th>
                                                    <th>Amount</th>
                                                    <th>Date</th>
                                                    <th>Reverse Payment</th>
                                                </tr>
                                                <tr v-for="(payment, index) in paymentsMade" v-bind:key="index">
                                                    <td>{{ payment.id }}</td>
                                                    <td>{{ payment.supplier.business_name }}</td>
                                                    <td>TZS {{ payment.amount | currency }}</td>
                                                    <td>{{ payment.created | date }}</td>
                                                    <td><a class="button is-danger" @click="deletePayment(payment.id)"><font-awesome-icon class="icon has-text-white" icon="times" size="sm"/></a></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="content is-vcentered notification" v-else>
                                        <p class="is-centered">No payments to show</p>
                                    </div>
                                </div>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pagesPayment.prev==false" @click="getPaymentsMade(pagesPayment.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="pagesPayment.next==false" @click="getPaymentsMade(pagesPayment.page+1)">Next page</a>
                                </footer>
                            </div>
                        </div>
                    </div>


                    <div class="columns">
                        <div class="column">
                            <div class="card events-card">
                                <header class="card-header">
                                    <p class="card-header-title">
                                        Procurements without Invoices
                                    </p>
                                </header>
                                <div class="card-table" style="height:500px">
                                    <div class="content" v-if="outstandingUninvoiced && outstandingUninvoiced.length> 0">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr>
                                                    <th>Procurement Id</th>
                                                    <th>Product</th>
                                                    <th>Supplier Id</th>
                                                    <th>Quantity</th>
                                                    <th>Total Cost</th>
                                                    <th>Date</th>
                                                    <th>Record as Paid</th>
                                                </tr>
                                                <tr v-for="(payment, index) in outstandingUninvoiced" v-bind:key="index">
                                                    <td>{{ payment.id }}
                                                    <td>{{ payment.product.description }} ({{ payment.product.sku }})</td>
                                                    <td>{{ payment.supplier }}</td>
                                                    <td>{{ payment.quantity }}
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td>{{ payment.created | date }}
                                                    <td><a class="button is-primary" @click="recordUninvoicedPayment(index)"><font-awesome-icon class="icon has-text-white" icon="check" size="sm" /></a></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="content is-vcentered notification" v-else>
                                        <p class="is-centered">No uninvoiced procurements to show</p>
                                    </div>
                                </div>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pagesUninvoiced.prev==false" @click="getOutstandingUninvoiced(pagesUninvoiced.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="pagesUninvoiced.next==false" @click="getOutstandingUninvoiced(pagesOutstanding.page+1)">Next page</a>
                                </footer>
                            </div>
                        </div>
                    </div>


                </div>
            </article>
        </div>
    </div>
</template>

<script>
var numeral = require("numeral");
import moment from 'moment'

export default {
    name: 'payments-view',
    components: {
    },
    data() {
        return {
            editing: null,
            response: null,
            errorNotification: null,
            outstandingPayments: [],
            pagesOutstanding: {
                page: null,
                next: null,
                prev: null
            },
            paymentsMade: [],
            pagesPayment: {
                page: null,
                next: null,
                prev: null
            },
            outstandingUninvoiced: [],
            pagesUninvoiced: {
                page: null,
                next: null,
                prev: null
            },
            stats: null,
            jwt: ''
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
    created() {
        this.jwt = this.$store.state.jwt
        this.handleSubmit()
    },
    methods: {
        handleSubmit() {
            this.getOutstandingPayments(1)
            this.getOutstandingUninvoiced(1)
            this.getPaymentsMade(1)
            this.getPaymentStats()            
        },
        getOutstandingPayments(page) {
            try {
                this.axios.get('payments/due?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.outstandingPayments = response.data[0].body
                        if (this.outstandingPayments) {
                            this.outstandingPayments = this.filterUniqueInvoices(this.outstandingPayments)
                        }
                        this.pagesOutstanding.page = response.data[0].page
                        this.pagesOutstanding.next = response.data[0].next
                        this.pagesOutstanding.prev = response.data[0].prev
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
        filterUniqueInvoices(outstandingPayments) {
            for (var i=0; i < outstandingPayments.length; i++) {
                var all_invoices = outstandingPayments[i]['invoices']
                var unique_invoices = []
                for (var j=0; j < all_invoices.length; j++) {
                    if (!unique_invoices.includes(all_invoices[j])) {
                        unique_invoices.push(all_invoices[j])
                    }
                }
                outstandingPayments[i]['invoices'] = unique_invoices
            }
            return outstandingPayments
        },
        getOutstandingUninvoiced(page) {
            try {
                this.axios.get('payments/due/uninvoiced?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.outstandingUninvoiced = response.data[0].body
                        this.pagesUninvoiced.page = response.data[0].page
                        this.pagesUninvoiced.next = response.data[0].next
                        this.pagesUninvoiced.prev = response.data[0].prev
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
        getPaymentsMade(page) {
            try {
                this.axios.get('payments/made?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.paymentsMade = response.data[0].body
                        this.pagesPayment.page = response.data[0].page
                        this.pagesPayment.next = response.data[0].next
                        this.pagesPayment.prev = response.data[0].prev
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
        getPaymentStats() {
            try {
                this.axios.get('payments/stats', { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.stats = response.data[0].body
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
        recordInvoicedPayment(index) {
            try {
                var outstandingInvoices = this.outstandingPayments[index]
                this.axios.post('payments', {'body': outstandingInvoices, 'from': 'view-invoiced'}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.handleSubmit()
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
        recordUninvoicedPayment(index) {
            try {
                var outstandingUninvoiced = this.outstandingUninvoiced[index]
                this.axios.post('payments', {'body': outstandingUninvoiced, 'from': 'view-uninvoiced'}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.handleSubmit()
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
        deletePayment(id) {
            try {
                this.axios.delete('payment/'+id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.handleSubmit()
                    }
                })
                .catch(error => {
                    this.response = error
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
button {
    margin: 0 0.5 rem 0;
}
.font-margin {
    margin: 0px 5px 0px 0px;
}
</style>