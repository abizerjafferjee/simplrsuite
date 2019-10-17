<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="level">
                    <div class="level-left">
                        <p class="title">All Suppliers</p>
                    </div>
                    <div class="level-right">
                        <!-- <p class="level-item"><a class="button" @click="show">Add Supplier</a></p> -->
                        <p class="level-item"><router-link to="/add-supplier" class="button">Add Supplier</router-link></p>
                    </div>
                </nav>
                <!-- <modal name="add-supplier" :width="800" :height="860" style="overflow-y:auto;"><supplier-form></supplier-form></modal> -->


                <!-- <p v-if="suppliers.length < 1" class="empty-table">No Suppliers</p> -->
                <div v-if="suppliers && suppliers.length < 1" class="notification">
                    You have no suppliers. Click Add Supplier to add your first supplier.
                </div>

                <div class="content" v-else>
                    <div class="field is-grouped notification">
                        <p class="control is-expanded">
                            <input v-model="search.text" class="input" type="text" placeholder="Search Suppliers">
                        </p>
                        <p class="control">
                            <a @click="getSuppliers(1)" class="button is-info">
                            Search
                            </a>
                        </p>
                    </div>

                    <div v-for="supplier in suppliers" :key="supplier.id">
                        <div class="box" style="margin:0px 0px 10px 0px">
                            <article class="media">
                                <div class="media-content">
                                    <div class="content">
                                        <p class="title is-4">
                                            <router-link :to="{ path: '/supplier-detail', query: {supplierId: supplier.id}}">{{ supplier.business_name }}</router-link> 
                                            <small>@{{ supplier.contact_person }}</small>
                                        </p>
                                        <p class="subtitle is-6">{{ supplier.email }} {{ supplier.phone }}</p>
                                    </div>
                                    <nav class="level is-mobile">
                                        <div class="level-left">
                                        <a class="level-item" aria-label="transactions">
                                            <button class="button is-small is-success">Payments</button>
                                        </a>
                                        <a class="level-item" aria-label="transactions">
                                            <button class="button is-small is-success">Procurements</button>
                                        </a>
                                        <a class="level-item" aria-label="edit">
                                            <button class="button is-small is-primary"><router-link :to="{ path: '/add-supplier', query: {editSupplier: supplier.id}}">Edit</router-link></button>
                                        </a>
                                        <a class="level-item" aria-label="delete">
                                            <button class="button is-small is-danger">Delete</button>
                                        </a>
                                        </div>
                                    </nav>
                                </div>
                            </article>
                        </div>
                    </div>

                    <br>
                    <nav class="pagination" role="navigation" aria-label="pagination">
                        <a class="button pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getSuppliers(pages.page-1)">Previous</a>
                        <a class="button pagination-next" :disabled="pages.next==false" @click="getSuppliers(pages.page+1)">Next page</a>
                    </nav>
                </div>
            </article>
        </div>
    </div>
</template>

<script>
import SupplierForm from '@/components/SupplierForm.vue'

export default {
    name: 'supplier-view',
    components: {
       SupplierForm
    },
    data() {
        return {
            suppliers: [],
            pages: {
                page: null,
                next: null,
                prev: null
            },
            search: {
                text: ''
            },
            editing: null,
            response: null,
        }
    },
    created() {
        this.getSuppliers(1)
    },
    methods: {
        getSuppliers(page) {
            try {
                this.axios.get('http://localhost:5000/suppliers?page='+page+'&search='+this.search.text)
                .then(response => {
                    this.suppliers = response.data[0].body
                    this.pages.page = response.data[0].page
                    this.pages.next = response.data[0].next
                    this.pages.prev = response.data[0].prev
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        show () {
           this.$modal.show('add-supplier');
        },
        editMode(product) {
            this.cachedProduct = Object.assign({}, product);
            this.editing = product.id
        },
        cancelEdit(product) {
            Object.assign(product, this.cachedProduct)
            this.editing = null
        },
        editProduct(updatedProduct) {
            try {
                this.axios.put('http://localhost:5000/products/edit?id='+updatedProduct.id, {'product': updatedProduct}, {'Content-Type': 'application/json'})
                .then(response => {
                    this.response = response
                    this.products = this.products.map(product => product.id === updatedProduct.id ? product: updatedProduct)
                })
                .catch(error => {
                    this.response = error
                })
            } catch(error) {
                this.response = error
            }
        },
        deleteProduct(id) {
            try {
                this.axios.delete('http://localhost:5000/products/delete?id='+id)
                .then(response => {
                    this.response = response
                    this.products = this.products.filter(product => product.id !== id);
                })
                .catch(error => {
                    this.response = error
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