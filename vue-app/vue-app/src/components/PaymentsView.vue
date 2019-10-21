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
                        <div class="tile is-ancestor has-text-centered">
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">439k</p>
                                    <p class="subtitle">Total Outstanding Amount</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">59k</p>
                                    <p class="subtitle">Total Outstanding Invoices</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">3.4k</p>
                                    <p class="subtitle">Total Procurements without Invoices</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">
                                    <p class="title">19</p>
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
                                        Outstanding Payments
                                    </p>
                                </header>
                                <div class="card-table" style="height:500px">
                                    <div class="content">
                                        <table class="table is-fullwidth is-striped">
                                            <tbody>
                                                <tr v-for="(payment, index) in outstandingPayments" v-bind:key="index">
                                                    <td width="5%"><i class="fa fa-bell-o"></i></td>
                                                    <td>{{ payment.business_name }} ({{ payment.supplier_id }})</td>
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td>{{ payment.invoices.length }} Invoices</td>
                                                    <td><a class="button is-small is-primary" href="#">Action</a></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pagesOutstanding.prev==false" @click="getOutstandingPayments(pagesOutstanding.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="pagesOutstanding.next==false" @click="getSuppliers(pagesOutstanding.page+1)">Next page</a>
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
                                                <tr v-for="(payment, index) in outstandingPayments" v-bind:key="index">
                                                    <td width="5%"><i class="fa fa-bell-o"></i></td>
                                                    <td>{{ payment.business_name }} ({{ payment.supplier_id }})</td>
                                                    <td>TZS {{ payment.total_cost | currency }}</td>
                                                    <td>{{ payment.invoices.length }} Invoices</td>
                                                    <td><a class="button is-small is-primary" href="#">Action</a></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pagesOutstanding.prev==false" @click="getOutstandingPayments(pagesOutstanding.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="pagesOutstanding.next==false" @click="getSuppliers(pagesOutstanding.page+1)">Next page</a>
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
import Tooltip from 'vue-bulma-tooltip'

export default {
    name: 'payments-view',
    components: {
        Tooltip
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
        }
    },
    filters: {
        currency: function (value) {
            return numeral(value).format("0,0")
        }
    },
    mounted() {
        this.getOutstandingPayments(1)
    },
    methods: {
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
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>