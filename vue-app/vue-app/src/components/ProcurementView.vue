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
    mounted() {
        this.getProcurements(1)
    },
    methods: {
        getProcurements(page) {
            try {
                this.axios.get('http://localhost:5000/procurement?page='+page)
                .then(response => {
                    this.procurements = response.data[0].body
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
                this.axios.put('http://localhost:5000/procurement?id='+updatedProcurement.id, {'body': updatedProcurement}, {'Content-Type': 'application/json'})
                .then(response => {
                    this.response = response
                    this.procurements = this.procurements.map(procurements => procurements.id === updatedProcurement.id ? procurements: updatedProcurement)
                    this.editing = null
                })
                .catch(error => {
                    this.response = error
                })
            } catch(error) {
                this.response = error
            }
        },
        deleteProcurement(id) {
            try {
                this.axios.delete('http://localhost:5000/procurement?id='+id)
                .then(response => {
                    this.response = response
                    // this.procurements = this.procurements.filter(procurements => procurement.id !== id);
                    this.getProcurements(this.procurementPages.page)
                })
                .catch(error => {
                    this.response = error
                })
            } catch (error) {
                this.response = error
            }
        },
        // getCategories() {
        //     this.axios.get('http://localhost:5000/categories')
        //     .then(response => {
        //         this.categories = response.data[0]['categories']
        //     })
        //     .catch(error => {
        //         this.response = error
        //     })
        // },
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>