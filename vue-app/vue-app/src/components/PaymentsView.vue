<template>
    <div id="payments-view">

        <div class="section">
            <div class="notification" v-if="error">
                <!-- <button @click="closeNotification" class="delete"></button> -->
                {{ error }}
            </div>
            <div v-else></div>
        </div>

        <article class="card has-text-centered">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column is-three-fifths">
                        <div class="field is-grouped is-expanding">
                            <div class="control is-expanded">
                                <model-select class="input is-large" ref="search" :options="supplierList" v-model="search" placeholder="search suppliers"></model-select>
                            </div>
                            <div class="control button is-primary">search</div>
                        </div>
                    </div>
                    <div class="column"></div>
                </div>
            </div>
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column">Supplier</div>
                    <div class="column">Invoice Number</div>
                    <div class="column">Payment Method</div>
                    <div class="column">Transaction Details</div>
                    <div class="column">Receipt</div>
                    <div class="column">Date</div>
                </div>
            </div>
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="payments && payments.length===0">You don't have a payment history. View your outstanding invoices and record payments.</div>
                <div class="card is-paddingless" v-for="(payment, index) in payments" v-bind:key="index" v-else-if="payments && payments.length > 0">
                    <div class="level">
                        <div class="column"><div class="title is-6">{{ payment.payment.supplier.business_name }}</div></div>
                        <div class="column"><div class="title is-6 has-text-info">{{ payment.payment.invoice_number }}</div></div>
                        <div class="column">
                            <div class="title is-6" v-if="payment.payment_type === 'BANK'">Bank Transfer</div>
                            <div class="title is-6" v-else-if="payment.payment_type === 'CHEQUE'">Cheque</div>
                            <div class="title is-6" v-else-if="payment.payment_type === 'CASH'">Cash</div>
                            <div class="title is-6" v-else>No Payment Method</div>
                        </div>
                        <div class="column">
                            <div class="title is-6" v-if="payment.payment_type === 'BANK' && payment.bank_transfer">{{ payment.bank_transfer }}</div>
                            <div class="title is-6" v-else-if="payment.payment_type === 'CHEQUE' && payment.cheque">{{ payment.cheque }}</div>
                            <div class="title is-6" v-else>No Transaction Details</div>
                        </div>

                        <div class="column">
                            <div class="title is-6" v-if="payment.receipt">{{ payment.receipt }}</div>
                            <div class="title is-6" v-else>No Receipt</div>
                        </div>

                        <div class="column">
                            <div class="title is-6" v-if="payment.date">{{ payment.date }}</div>
                            <div class="title is-6" v-else>No Date</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getPayments(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getPayments(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>

        <!-- <section class="info-tiles">
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
        </section> -->

    </div>
</template>

<script>
var numeral = require("numeral");
import moment from 'moment'
import { ModelSelect } from 'vue-search-select';
export default {
    name: 'payments-view',
    components: {
        ModelSelect,
    },
    data() {
        return {
            jwt: '',
            editing: null,
            response: null,
            error: null,
            stats: null,
            payments: null,
            pages: {
                page: null,
                next: null,
                prev: null
            },
            search: null,
            supplierList: [],
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
        this.getPayments(1)
        this.getSupplierList()
    },
    methods: {
        getPayments(page) {
            this.axios.get('payments?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.payments = response.data.body
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
        getSupplierList(){
            this.axios.get('suppliers/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.supplierList = response.data.suppliers
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        getPaymentStats() {
            this.axios.get('payments/stats', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.stats = response.data.body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },

        closeNotification() {
            this.error = null
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