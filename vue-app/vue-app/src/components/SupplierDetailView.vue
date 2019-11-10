<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/suppliers">Suppliers</router-link></li>
                    <li class="is-active">
                        <a aria-current="page">Supplier Details</a>
                    </li>
                </ul>
                </nav>

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 v-if="supplier" class="title level-left">
                                {{ supplier.business_name }}
                            </h1>
                            <h3 v-else>Supplier information could not load</h3>
                        </div>
                    </div>
                </section>
                <br>

                <section class="info-tiles">
                    <!-- <div class="tile is-ancestor has-text-centered" v-if="stats">
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
                    </div> -->
                </section>
                <br>

                <div class="columns">
                    <div class="column">
                        <div class="card events-card">
                            <header class="card-header level">
                                <div class="card-header-title level-left level-item">Supplier Details</div>
                                <div class="level-right has-margin-10">
                                    <button v-if="editSupplier" class="button is-small is-success level-item" @click="saveSupplier()"><span><font-awesome-icon class="font-margin" icon="save" size="lg" /></span> save</button>
                                    <button v-if="editSupplier" class="button is-small is-white level-item" @click="cancelEdit('supplier')">cancel</button>
                                    <button class="button is-small is-link level-item" @click="editMode('supplier')" v-else><font-awesome-icon class="font-margin" icon="pen-square" size="lg" />edit</button>
                                    <div></div>
                                </div>
                            </header>
                            <div class="card-table" v-if="supplier" id="supplier-table">
                                <table class="table is-fullwidth is-striped">
                                    <tbody>
                                        <tr>                                             
                                            <th>Supplier Id</th>
                                            <td>{{ supplier.id }}</td>
                                        </tr>
                                        <tr>                                             
                                            <th>Supplier Name</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.business_name"></td>
                                            <td v-else>{{ supplier.business_name }}</td>
                                        </tr>
                                        <tr>
                                            <th>Contact Person</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.contact_person"></td>
                                            <td v-else>{{ supplier.contact_person }}</td>
                                        </tr>
                                        <tr>
                                            <th><font-awesome-icon class="font-margin" icon="envelope-square" size="lg" />Email Address</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.email"></td>
                                            <td v-else>{{ supplier.email }}</td>
                                        </tr>
                                        <tr>
                                            <th><font-awesome-icon class="font-margin" icon="phone-square-alt" size="lg" />Phone Number</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.phone"></td>
                                            <td v-else>{{ supplier.phone }}</td>
                                        </tr>
                                        <tr>
                                            <th><font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />Plus Code</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.plus_code"></td>
                                            <td v-else>{{ supplier.plus_code }}</td>
                                        </tr>
                                        <tr>
                                            <th><font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />Address</th>
                                            <td v-if="editSupplier"><input class="input" type="text" v-model="supplier.address"></td>
                                            <td v-else>{{ supplier.address }}</td>
                                        </tr>
                                        <tr>
                                            <th>Additional Info</th>
                                            <td v-if="editSupplier"><textarea class="textarea" type="text" v-model="supplier.additional_info"></textarea></td>
                                            <td v-else>{{ supplier.additional_info }}</td>
                                        </tr>
                                        <tr>
                                            <th>Created</th>
                                            <td>{{ supplier.created | date }}</td>
                                        </tr>
                                        <tr>
                                            <th>Total Procurement Records</th>
                                            <td>{{ supplier.procurements.length }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="content" v-else><p class="notification">Supplier information failed to load.</p></div>
                        </div>
                    </div>

                    <div class="column">
                        <div class="card events-card">
                            <header class="card-header">
                                <p class="card-header-title">
                                    Payments Made
                                </p>
                            </header>
                            <div class="card-table" id="payment-table">
                                <div class="content" v-if="payments">
                                    <table class="table is-fullwidth is-striped" v-if="payments.length > 0">
                                        <tbody>
                                            <tr>
                                                <th>Payment Id</th>
                                                <th>Invoices/ Procurement Id</th>
                                                <th>Amount</th>
                                                <th>Date</th>
                                            </tr>
                                            <tr v-for="payment in payments" v-bind:key="payment.id">
                                                <td>{{ payment.id }}</td>
                                                <td v-if="payment.invoiced">{{ parseInvoiceInfo(payment.invoices) }}</td>
                                                <td v-else>PID {{ payment.procurements }}</td>
                                                <td>TZS {{ payment.amount | currency }}</td>
                                                <td>{{ payment.created | date }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <p class="title" v-else>No payments have been made.</p>
                                </div>
                            </div>
                            <footer class="card-footer level">
                                <a class="pagination-previous level-left" title="This is the first page" :disabled="paymentPages.prev==false" @click="getPayments(paymentPages.page-1)">Previous</a>
                                <a class="pagination-next level-right" :disabled="paymentPages.next==false" @click="getPayments(paymentPages.page+1)">Next page</a>
                            </footer>
                        </div>
                    </div>
                </div>

                <div class="columns">
                    <div class="column">
                        <div class="card events-card">
                            <header class="card-header"><p class="card-header-title">Procurements</p></header>
                            <div class="card-table" v-if="procurement">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Procurement Id</th>
                                            <th>Product</th>
                                            <th>SKU</th>
                                            <th>Invoice</th>
                                            <th>Quantity</th>
                                            <th>Unit Cost</th>
                                            <th>Total Cost</th>
                                            <th>Location</th>
                                            <th>Date</th>
                                            <th>Paid</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="p in procurement" :key="p.id">
                                        <td>{{ p.id }}</td>
                                        <td>{{ p.product.description }}</td>
                                        <td>{{ p.product.sku }}</td>
                                        <td>{{ p.invoice }}</td>
                                        <td>{{ p.quantity }}</td>
                                        <td>{{ p.unit_cost | currency }}</td>
                                        <td>{{ p.total_cost | currency }}</td>
                                        <td>{{ p.location }}</td>
                                        <td>{{ p.created | date }}</td>
                                        <td><span v-bind:class="{'tag is-success': p.paid === 'Paid', 'tag is-danger': p.paid === 'Unpaid'}">{{ p.paid }}</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                                <footer class="card-footer level">
                                    <a class="pagination-previous level-left" title="This is the first page" :disabled="procurementPages.prev==false" @click="getProcurement(procurementPages.page-1)">Previous</a>
                                    <a class="pagination-next level-right" :disabled="procurementPages.next==false" @click="getProcurement(procurementPages.page+1)">Next page</a>
                                </footer>
                            </div>
                            <div v-else><p class="title notification">No Procurements found for this supplier</p></div>
                        </div>
                    </div>
                </div>

                <div class="columns">
                    <div class="column">
                        <div class="card events-card">
                            <header class="card-header"><p class="card-header-title">Invoices & Bulk Procurement</p></header>
                            <div class="card-table">
                                <!-- <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Procurement Id</th>
                                            <th>Product</th>
                                            <th>SKU</th>
                                            <th>Invoice</th>
                                            <th>Quantity</th>
                                            <th>Unit Cost</th>
                                            <th>Total Cost</th>
                                            <th>Location</th>
                                            <th>Date</th>
                                            <th>Paid</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="p in procurement" :key="p.id">
                                        <td>{{ p.id }}</td>
                                        <td>{{ p.product.description }}</td>
                                        <td>{{ p.product.sku }}</td>
                                        <td>{{ p.invoice }}</td>
                                        <td>{{ p.quantity }}</td>
                                        <td>{{ p.unit_cost }}</td>
                                        <td>{{ p.total_cost }}</td>
                                        <td>{{ p.created }}</td>
                                        <td>{{ p.location }}</td>
                                        <td><span class="tag is-info">{{ p.paid }}</span></td>
                                        </tr>
                                    </tbody>
                                </table> -->
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
    name: 'product-detail',
    data() {
        return {
            supplierId: null,
            supplier: null,
            editSupplier: false,
            procurement: null,
            procurementPages: {
                page: null,
                next: null,
                prev: null
            },
            payments: null,
            paymentPages: {
                page: null,
                next: null,
                prev: null
            },
            response: null,
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
        if (this.$route.query.supplierId) {
            this.supplierId = this.$route.query.supplierId
            this.getSupplier()
        }
    },
    methods: {
        editMode(info) {
            if (info === 'supplier') {
                this.editSupplier = true
                this.cachedSupplier = Object.assign({}, this.supplier);
            }
        },
        cancelEdit(info) {
            if (info === 'supplier') {
                this.editSupplier = false
                Object.assign(this.supplier, this.cachedSupplier)
            }
        },
        getSupplier() {
            try {
                this.axios.get('http://localhost:5000/suppliers/'+this.supplierId)
                .then(response => {
                    this.supplier = response.data[0].body
                    this.getProcurement(1)
                    this.getPayments(1)
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        saveSupplier() {
            try {
                this.axios.put('http://localhost:5000/products?id='+this.supplier.id, {'body': this.supplier}, {'Content-Type': 'application/json'})
                .then(response => {
                    this.response = response
                    this.cachedSupplier = Object.assign({}, this.supplier);
                    this.cancelEdit('supplier')
                })
                .catch(error => {
                    this.response = error
                })
            } catch(error) {
                this.response = error
            }
        },
        getProcurement(page) {
            try {
                this.axios.get('http://localhost:5000/procurement/supplier/'+this.supplier.id+'?page='+page)
                .then(response => {
                    this.procurement = response.data[0].body
                    this.procurementPages.page = response.data[0].page
                    this.procurementPages.next = response.data[0].next
                    this.procurementPages.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        getPayments(page) {
            try {
                this.axios.get('http://localhost:5000/payments/supplier/'+this.supplier.id+'?page='+page)
                .then(response => {
                    this.payments = response.data[0].body
                    this.paymentPages.page = response.data[0].page
                    this.paymentPages.next = response.data[0].next
                    this.paymentPages.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        parseInvoiceInfo(invoices) {
            invoices = invoices.split(',')
            var parsed = []
            for (var i=0; i < invoices.length; i++) {
                var a = invoices[i].replace('{', '')
                a = a.replace('}', '')
                if (!parsed.includes(a,0)) {
                    parsed.push(a)
                }
            }
            return parsed.toString()
        },
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
#payment-table {
    height:520px;
}
#supplier-table {
    height: 550px;
    overflow-y: auto;
}
</style>