<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/products">Products</router-link></li>
                    <li class="is-active">
                        <a href="#" aria-current="page">Product Details</a>
                    </li>
                </ul>
                </nav>

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 v-if="product" class="title level-left">
                                {{ product.description }}
                            </h1>
                            <h3 v-else>Product Loading...</h3>
                        </div>
                    </div>
                </section>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>

                <div class="columns">
                    <div class="column" v-if="product">
                        <img :src="require('../assets/uploads/' + product.image_path)" v-if="product.image_path">
                        <img heigth=300 src="../assets/ecommerce-default-product.png" alt="Placeholder image" v-else>
                    </div>
                    <div class="column" v-else>
                        <img heigth=300 src="../assets/ecommerce-default-product.png" alt="Placeholder image">
                    </div>
                    <div class="column is-8">
                        <div class="card events-card">
                            <header class="card-header level">
                                <div class="card-header-title level-left level-item">Product Details</div>
                                <div class="level-right">
                                    <button v-if="editProduct" class="button is-small is-success level-item" @click="saveProduct()"><font-awesome-icon class="font-margin" icon="save" size="lg" />save</button>
                                    <button v-if="editProduct" class="button is-small is-white level-item" @click="cancelEdit('product')">cancel</button>
                                    <button class="button is-small is-link level-item" @click="editMode('product')" v-else><font-awesome-icon class="font-margin" icon="pen-square" size="lg" />edit</button>
                                    <div></div>
                                </div>
                            </header>
                            <div class="card-table" v-if="product">
                                <table class="table is-fullwidth is-striped">
                                    <tbody>
                                        <tr>                                             
                                            <th>Product Name</th>
                                            <td v-if="editProduct"><input class="input" type="text" v-model="product.description"></td>
                                            <td v-else>{{ product.description }}</td>
                                        </tr>
                                        <tr>
                                            <th>Product Type</th>
                                            <td v-if="editProduct"><input class="input" type="text" v-model="product.product_type"></td>
                                            <td v-else>{{ product.product_type }}</td>
                                        </tr>
                                        <tr>
                                            <th>Category</th>
                                            <td>{{ product.category.name }}</td>
                                        </tr>
                                        <tr>
                                            <th>Product SKU</th>
                                            <td>{{ product.sku }}</td>
                                        </tr>
                                        <tr>
                                            <th>Packing</th>
                                            <td>{{ product.packing_type }}</td>
                                        </tr>
                                        <tr>
                                            <th>Additional Packing</th>
                                            <td v-if="editProduct"><input class="input" type="text" v-model="product.packing"></td>
                                            <td v-else>{{ product.packing }}</td>
                                        </tr>
                                        <tr>
                                        <th>Additional Information</th>
                                            <td v-if="editProduct"><textarea class="textarea" type="text" v-model="product.additional_info"></textarea></td>
                                            <td v-else>{{ product.additional_info }}</td>
                                        </tr>
                                        <tr>
                                            <th>Created</th>
                                            <td>{{ product.created | date }}</td>
                                        </tr>
                                        <tr v-if="inventory">
                                            <th>Quantity in Stock</th>
                                            <div class="level">
                                                <td v-if="editInventory" class="level-left level-item"><input class="input" type="number" v-model="inventory.quantity"></td>
                                                <td v-else class="level-left level-item">{{ inventory.quantity }}</td>
                                                <td v-if="editInventory" class="level-right level-item">
                                                    <button class="button is-small is-success" @click="saveInventory()"><font-awesome-icon class="font-margin" icon="save" size="lg" />save</button>
                                                    <button class="button is-small is-white" @click="cancelEdit('inventory')">cancel</button>
                                                </td>
                                                <td v-else class="level-right level-item">
                                                    <button class="button is-small is-link level-item" @click="editMode('inventory')"><font-awesome-icon class="font-margin" icon="pen-square" size="lg" />edit</button>
                                                </td>   
                                            </div> 
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div class="content" v-else><p class="notification">Product Information failed to load.</p></div>
                        </div>
                    </div>
                </div>

                <div class="columns">
                    <div class="column">
                        <div class="card events-card">
                            <header class="card-header"><p class="card-header-title">Procurements</p></header>
                            <div class="card-table">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Supplier</th>
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
                                        <tr v-for="p in procurement" :key="p.id">
                                        <td>{{ p.supplier }}</td>
                                        <td>{{ p.invoice }}</td>
                                        <td>{{ p.quantity }}</td>
                                        <td>{{ p.currency }}</td>
                                        <td>{{ p.unit_cost | currency }}</td>
                                        <td>{{ p.total_cost | currency }}</td>
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
            response: null,
            errorNotification: null,
            productId: null,
            product: null,
            inventoryId: null,
            inventory: null,
            editProduct: false,
            editInventory: false,
            procurement: null,
            procurementPages: {
                page: null,
                next: null,
                prev: null
            },
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
        if (this.$route.query.productId) {
            this.productId = this.$route.query.productId
            this.getProduct()
        }
    },
    methods: {
        editMode(info) {
            if (info === 'inventory') {
                this.editInventory = true
                this.cachedInventory = Object.assign({}, this.inventory);
            } else if (info === 'product') {
                this.editProduct = true
                this.cachedProduct = Object.assign({}, this.product);
            }
        },
        cancelEdit(info) {
            if (info === 'inventory') {
                this.editInventory = false
                Object.assign(this.inventory, this.cachedInventory)
            } else if (info === 'product') {
                this.editProduct = false
                Object.assign(this.product, this.cachedProduct)
            }
        },
        getProduct() {
            try {
                this.axios.get('http://localhost:5000/products/'+this.productId, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.product = response.data[0].body
                        this.inventoryId = this.product['inventory'][0]
                        if (this.inventoryId) {
                            this.getInventory()
                        }
                        this.getProcurement(1)
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
        getInventory() {
            try {
                this.axios.get('http://localhost:5000/inventory/'+this.inventoryId, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.inventory = response.data[0].body
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
        saveProduct() {
            try {
                this.axios.put('http://localhost:5000/products?id='+this.product.id, {'body': this.product}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.cachedProduct = Object.assign({}, this.product);
                        this.cancelEdit('product')
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
        saveInventory() {
            try {
                this.axios.put('http://localhost:5000/inventory?id='+this.inventory.id, {'body': this.inventory}, { headers: {'Content-Type': 'multipart/form-data', 'Authorization': `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.cachedInventory = Object.assign({}, this.inventory);
                        this.cancelEdit('inventory')
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
        getProcurement(page) {
            try {
                this.axios.get('http://localhost:5000/procurement/product/'+this.product.id+'?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] == 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.procurement = response.data[0].body
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
.font-margin {
    margin: 0px 5px 0px 0px;
}
</style>