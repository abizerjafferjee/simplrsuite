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
            this.axios.get('products/'+this.productId, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.product = response.data.body
                this.inventoryId = this.product['inventory'][0]
                if (this.inventoryId) {
                    this.getInventory()
                }
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        getInventory() {
            this.axios.get('inventory/'+this.inventoryId, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.inventory = response.data[0].body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        saveProduct() {
            this.axios.put('products?id='+this.product.id, {'body': this.product}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.cachedProduct = Object.assign({}, this.product);
                this.cancelEdit('product')
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        saveInventory() {
            this.axios.put('inventory?id='+this.inventory.id, {'body': this.inventory}, { headers: {'Content-Type': 'multipart/form-data', 'Authorization': `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.cachedInventory = Object.assign({}, this.inventory);
                this.cancelEdit('inventory')
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