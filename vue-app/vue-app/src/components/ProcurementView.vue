<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 class="title level-left">
                                Procurements & Inventory
                            </h1>
                            <div class="level-right">
                                <p class="level-item"><router-link to="/add-inventory" class="button">Add Inventory</router-link></p>
                            </div>
                        </div>
                    </div>
                </section>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>

                <div v-if="procurements && procurements.length < 1" class="notification">
                    You have no Inventory or associated Procurement record. Click Add Inventory to add your first inventory.
                </div>

                <div class="content" v-else>

                    <p class="notification">Your 10 latest procurements.</p>

                    <table class="table">
                        <thead>
                            <tr>
                            <th>Product</th>
                            <th>Supplier Id</th>
                            <th>Invoice</th>
                            <th>Quantity</th>
                            <th>Currency</th>
                            <th>Unit Cost</th>
                            <th>Total Cost</th>
                            <th>Date</th>
                            <th>Paid</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="procurement in procurements" :key="procurement.id">
                            <td>{{ procurement.product.description }}</td>
                            <td>{{ procurement.supplier }}</td>
                            <td v-if="editing === procurement.id"><input type="text" v-model="procurement.invoice"></td>
                            <td v-else>{{ procurement.invoice }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.quantity"></td>
                            <td v-else>{{ procurement.quantity }}</td>
                            <td>{{ procurement.currency }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.unit_cost"></td>
                            <td v-else>{{ procurement.unit_cost | currency }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.total_cost"></td>
                            <td v-else>{{ procurement.total_cost | currency }}</td>
                            <td>{{ procurement.created | date }}</td>
                            <td><span v-bind:class="{'tag is-success': procurement.paid === 'Paid', 'tag is-danger': procurement.paid === 'Unpaid'}">{{ procurement.paid }}</span></td>
                            <td v-if="editing == procurement.id">
                                <button class="button is-small is-success" @click="editProcurement(procurement)">save</button>
                                <button class="button is-small muted-button" @click="cancelEdit(procurement)">cancel</button>
                            </td>
                            <td v-else>
                                <button class="button is-small is-primary" @click="editMode(procurement)">edit</button>
                                <button class="button is-small is-danger" @click="deleteProcurement(procurement.id)">delete</button>
                            </td>
                            </tr>
                        </tbody>
                    </table>

                    <footer class="card-footer level">
                        <a class="pagination-previous level-left" title="This is the first page" :disabled="procurementPages.prev==false" @click="getProcurements(procurementPages.page-1)">Previous</a>
                        <a class="pagination-next level-right" :disabled="procurementPages.next==false" @click="getProcurements(procurementPages.page+1)">Next page</a>
                    </footer>
                </div>
            </article>
        </div>
    </div>
</template>

<script>
var numeral = require("numeral");
import moment from 'moment'
export default {
    name: 'procurement-table',
    data() {
        return {
            procurements: [],
            procurementPages: {
                page: null,
                next: null,
                prev: null
            },
            editing: null,
            response: null,
            errorNotification: null,
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
        this.getProcurements(1)
    },
    methods: {
        getProcurements(page) {
            try {
                this.axios.get('procurement?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.procurements = response.data[0].body
                        this.procurementPages.page = response.data[0].page
                        this.procurementPages.next = response.data[0].next
                        this.procurementPages.prev = response.data[0].prev
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
        editMode(procurement) {
            this.cachedProcurement = Object.assign({}, procurement);
            this.editing = procurement.id
        },
        cancelEdit(procurement) {
            Object.assign(procurement, this.cachedProcurement)
            this.editing = null
        },
        editProcurement(updatedProcurement) {
            try {
                this.axios.put('procurement?id='+updatedProcurement.id, {'body': updatedProcurement}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.procurements = this.procurements.map(procurements => procurements.id === updatedProcurement.id ? procurements: updatedProcurement)
                        this.editing = null
                    }
                })
                .catch(error => {
                    this.response = error
                    this.errorNotification = "Internal Server Error."
                })
            } catch(error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
        },
        deleteProcurement(id) {
            try {
                this.axios.delete('procurement?id='+id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        // this.procurements = this.procurements.filter(procurements => procurement.id !== id);
                        this.getProcurements(this.procurementPages.page)
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
</style>