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
                                    <p class="title">{{ stats.latest_payment.created | date }}</p>
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
                                    <div class="content">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr v-for="(payment, index) in outstandingPayments" v-bind:key="index">
                                                    <td>{{ payment.business_name }} ({{ payment.supplier_id }})</td>
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td>{{ payment.invoices.length }} Invoices</td>
                                                    <td><a class="button is-small is-primary" @click="recordInvoicedPayment(index)">Record as Paid</a></td>
                                                </tr>
                                            </tbody>
                                        </table>
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
                                    <div class="content">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr v-for="(payment, index) in paymentsMade" v-bind:key="index">
                                                    <td>{{ payment.id }}</td>
                                                    <td>{{ payment.supplier.business_name }}</td>
                                                    <td>TZS {{ payment.amount | currency }}</td>
                                                    <td>{{ payment.created | date }}</td>
                                                    <td><a class="button is-small is-danger">Revert</a></td>
                                                </tr>
                                            </tbody>
                                        </table>
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
                                    <div class="content">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr v-for="(payment, index) in outstandingUninvoiced" v-bind:key="index">
                                                    <td>{{ payment.id }}
                                                    <td>{{ payment.description }} ({{ payment.product.sku }})</td>
                                                    <td>{{ payment.supplier.business_name }} ({{ payment.supplier_id }})</td>
                                                    <td>{{ payment.quantity }}
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td>{{ payment.created | date }}
                                                    <td><a class="button is-small is-primary" @click="recordUninvoicedPayment(index)">Record as Paid</a></td>
                                                </tr>
                                            </tbody>
                                        </table>
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
            stats: null
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
                this.axios.get('http://localhost:5000/payments/due?page='+page)
                .then(response => {
                    this.outstandingPayments = response.data[0].body
                    this.pagesOutstanding.page = response.data[0].page
                    this.pagesOutstanding.next = response.data[0].next
                    this.pagesOutstanding.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        getOutstandingUninvoiced(page) {
            try {
                this.axios.get('http://localhost:5000/payments/due/uninvoiced?page='+page)
                .then(response => {
                    this.outstandingUninvoiced = response.data[0].body
                    this.pagesUninvoiced.page = response.data[0].page
                    this.pagesUninvoiced.next = response.data[0].next
                    this.pagesUninvoiced.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        getPaymentsMade(page) {
            try {
                this.axios.get('http://localhost:5000/payments/made?page='+page)
                .then(response => {
                    this.paymentsMade = response.data[0].body
                    this.pagesPayment.page = response.data[0].page
                    this.pagesPayment.next = response.data[0].next
                    this.pagesPayment.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        getPaymentStats() {
            try {
                this.axios.get('http://localhost:5000/payments/stats')
                .then(response => {
                    this.stats = response.data[0].body
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        recordInvoicedPayment(index) {
            try {
                var outstandingInvoices = this.outstandingPayments[index]
                this.axios.post('http://localhost:5000/payments', {'body': outstandingInvoices, 'from': 'view-invoiced'})
                .then(response => {
                    this.response = response
                    this.handleSubmit()
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        recordUninvoicedPayment(index) {
            try {
                var outstandingUninvoiced = this.outstandingUninvoiced[index]
                this.axios.post('http://localhost:5000/payments', {'body': outstandingUninvoiced, 'from': 'view-uninvoiced'})
                .then(response => {
                    this.response = response
                    this.handleSubmit()
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>