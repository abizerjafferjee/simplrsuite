<template>
    <div id="invoice-view">

        <div class="section">
            <div v-if="error" class="notification">
                <!-- <button @click="closeNotification" class="delete"></button> -->
                {{ error }}
            </div>
            <div></div>
        </div>

        <article class="card has-text-centered">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column is-two-fifths">
                        <div class="field is-grouped is-expanding">
                            <div class="control is-expanded">
                                <model-select class="input is-large" ref="search" :options="invoiceNumbers" v-model="invoiceSearch" placeholder="search invoices"></model-select>
                            </div>
                            <div class="control button is-primary">search</div>
                        </div>
                    </div>
                    <div class="column is-two-fifths"></div>
                    <div class="column">
                        <router-link to="/add-invoice" class="button">Add Invoice</router-link>
                    </div>
                </div>
            </div>
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column">Supplier</div>
                    <div class="column">Invoice Number</div>
                    <div class="column">Total Amount</div>
                    <div class="column">Delivered</div>
                    <div class="column">Items</div>
                    <div class="column">Invoice Date</div>
                </div>
            </div>
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="invoices && invoices.length === 0">You have 0 invoices. Click Add Invoice to add a new invoice.</div>
                <div class="card is-paddingless" v-for="(invoice, index) in invoices" v-bind:key="index" v-else-if="invoices && invoices.length > 0">
                    <div class="level">
                        <div class="column"><a @click="togglePurchaseDisplay(index)" class="title is-6 has-text-link">{{ invoice.supplier.business_name }}</a></div>
                        <div class="column"><div class="title is-6">{{ invoice.invoice_number }}</div></div>
                        <div class="column"><div class="title is-6">{{ invoice.currency }} {{ invoice.total_cost | currency }}</div></div>

                        <div class="column">
                            <div class="title is-6" v-if="invoice.delivery">Delivered {{ invoice.delivery }}</div>
                            <div class="title is-6 has-text-danger" v-else>Not Delivered</div>
                        </div>
                        <div class="column" v-if="invoice.items"><div class="title is-6">{{ invoice.items.length }}</div></div>
                        <div class="column">
                            <div class="title is-6" v-if="invoice.date">{{ invoice.date }}</div>
                            <div class="title is-6" v-else>No Date</div>
                        </div>
                    </div>
                    <div class="card" v-if="displayPurchases[index]">
                        <div class="card is-paddingless has-background-light">
                            <div class="level title is-6">
                                <div class="column is-two-fifths">Product</div>
                                <div class="column">Unit Cost</div>
                                <div class="column">Unit Tax</div>
                                <div class="column">Quantity</div>
                                <div class="column">Total Cost</div>
                            </div>
                        </div>
                        <div class="card is-paddingless has-background-light" v-for="(item, index) in invoice.items" v-bind:key="index" style="font-size: 15px;">
                            <div class="level">
                                <div class="column is-two-fifths"><div>{{ item.product.description }}</div></div>
                                <div class="column"><div>{{ item.currency }} {{ item.unit_cost | currency }}</div></div>
                                <div class="column"><div>{{ item.currency }} {{ item.unit_tax | currency }}</div></div>
                                <div class="column"><div>{{ item.quantity }}</div></div>
                                <div class="column"><div>{{ item.currency }} {{ item.total_cost | currency }}</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getInvoices(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getInvoices(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>
    </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select';
var numeral = require("numeral");
import moment from 'moment';
export default {
    name: 'procurement-table',
    components: {
        ModelSelect
    },
    data() {
        return {
            jwt: '',
            response: null,
            error: null,
            displayPurchases: [],
            invoiceNumbers: [],
            invoiceSearch: null,
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
        this.getInvoiceNumbers()
    },
    methods: {
        getInvoices(page) {
            this.axios.get('invoices?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.invoices = response.data.body
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev

                this.setPurchaseDisplay()
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        setPurchaseDisplay() {
            for (var i=0; i<this.invoices.length; i++) {
                this.displayPurchases.push(false)
            }
        },
        togglePurchaseDisplay(index) {
            var display = !this.displayPurchases[index]
            this.$set(this.displayPurchases, index, display)
        },
        getInvoiceNumbers() {
            this.axios.get('invoices/numbers', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.invoiceNumbers = response.data.body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })      
        },
        getInvoice() {
            if (this.invoiceSearch) {
                this.axios.get('invoices/'+this.invoiceSearch, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    this.invoiceNumbers = response.data.body
                })
                .catch(error => {
                    if (error.response.status === 401) {
                        this.error = "Your session has expired. Please login again."
                    } else {
                        this.error = "Internal Server Error"
                    }
                })
            }    
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