<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">
                <nav class="level">
                    <div class="level-left">
                        <p class="title">Procurement</p>
                    </div>
                    <div class="level-right">
                        <!-- <p class="level-item"><a class="button" @click="show">Add Supplier</a></p> -->
                        <p class="level-item"><router-link to="/add-inventory" class="button">Add Inventory</router-link></p>
                    </div>
                </nav>

                <div v-if="procurements && procurements.length < 1" class="notification">
                    You have no Inventory or associated Procurement record. Click Add Inventory to add your first inventory.
                </div>

                <div class="content" v-else>

                    <p class="notification">Your 10 latest procurements.</p>

                    <table class="table">
                        <thead>
                            <tr>
                            <th>Product</th>
                            <th>Supplier</th>
                            <th>Invoice</th>
                            <th>Quantity</th>
                            <th>Unit Cost</th>
                            <th>Total Cost</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="procurement in procurements" :key="procurement.id">
                            <td>{{ procurement.product.description }}</td>
                            <td v-if="procurement.supplier">{{ procurement.supplier.business_name }}</td>
                            <td v-else></td>
                            <td v-if="editing === procurement.id"><input type="text" v-model="procurement.invoice"></td>
                            <td v-else>{{ procurement.invoice }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.quantity"></td>
                            <td v-else>{{ procurement.quantity }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.unit_cost"></td>
                            <td v-else>{{ procurement.unit_cost }}</td>
                            <td v-if="editing === procurement.id"><input type="number" v-model="procurement.total_cost"></td>
                            <td v-else>{{ procurement.total_cost }}</td>
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

                    <!-- <nav class="pagination" role="navigation" aria-label="pagination">
                        <a class="button pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getprocurements(pages.page-1)">Previous</a>
                        <a class="button pagination-next" :disabled="pages.next==false" @click="getprocurements(pages.page+1)">Next page</a>
                    </nav> -->
                </div>
            </article>
        </div>
    </div>
</template>

<script>
export default {
    name: 'procurement-table',
    data() {
        return {
            procurements: [],
            editing: null,
            response: null,
        }
    },
    mounted() {
        this.getProcurements()
    },
    methods: {
        getProcurements() {
            try {
                this.axios.get('http://localhost:5000/procurement')
                .then(response => {
                    this.procurements = response.data[0].body
                    // console.log(this.procurements)
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
                    this.procurements = this.procurements.map(procurements => procurement.id === updatedProduct.id ? product: updatedProduct)
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
                    this.getProcurements()
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