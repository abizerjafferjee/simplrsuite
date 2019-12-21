<template>
    <div id="outstanding-invoices-view">

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
                    <div class="column is-four-fifths"></div>
                    <div class="column">
                        <router-link to="/record-payment" class="button is-link">Record Payment</router-link>
                    </div>
                </div>
            </div>
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column">Supplier</div>
                    <div class="column">Invoice Number</div>
                    <div class="column">Total Amount</div>
                    <div class="column">Payment Terms</div>
                    <div class="column">Invoice Date</div>
                </div>
            </div>
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="invoices && invoices.length===0">You have 0 invoices. Click Add Invoice to add a new invoice.</div>
                <div class="card is-paddingless" v-for="(invoice, index) in invoices" v-bind:key="index" v-else-if="invoices && invoices.length > 0">
                    <div class="level">
                        <div class="column"><div class="title is-6">{{ invoice.supplier.business_name }}</div></div>
                        <div class="column"><div class="title is-6 has-text-info">{{ invoice.invoice_number }}</div></div>
                        <div class="column"><div class="title is-6">{{ invoice.currency }} {{ invoice.total_cost | currency }}</div></div>

                        <div class="column">
                            <div class="title is-6" v-if="invoice.paid">Paid &nbsp;<font-awesome-icon class="font-margin has-text-success" icon="check-circle" size="lg" /></div>
                            <div class="title is-6 has-text-info" v-if="invoice.terms">Terms {{ invoice.terms }} Days</div>
                            <div class="title is-6 has-text-danger" v-else>No Terms</div >
                        </div>
                        <div class="column">
                            <div class="title is-6" v-if="invoice.date">{{ invoice.date }}</div>
                            <div class="title is-6" v-else>No Date</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getInvoices(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getInvoices(pages.page+1)">Next</a>
                </div>
            </div>
        </article>
        
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
            jwt: '',
            editing: null,
            response: null,
            error: null,
            stats: null,
            invoices: null,
            pages: {
                page: null,
                next: null,
                prev: null
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
    created() {
        this.jwt = this.$store.state.jwt
        this.getInvoices(1)
    },
    methods: {
        getInvoices(page) {
            this.axios.get('invoices/outstanding?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.invoices = response.data.body
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error."
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
                    this.error = "Internal Server Error."
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