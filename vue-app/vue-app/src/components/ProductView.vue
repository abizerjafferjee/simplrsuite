<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="level">
                    <div class="level-left">
                        <p class="title">All Products</p>
                    </div>
                    <div class="level-right">
                        <!-- <p class="level-item"><a class="button" @click="show">Add Supplier</a></p> -->
                        <p class="level-item"><router-link to="/add-product" class="button">Add Product</router-link></p>
                    </div>
                </nav>

                <!-- <p class="title">All Product</p> -->
                <!-- <p class="subtitle">View products, costs, quantities and prices.</p> -->

                <p v-if="products.length < 1" class="empty-table">No Products</p>
                <div class="content" v-else>
                    <div class="field is-grouped">
                        <p class="control is-expanded">
                            <input v-model="search.text" class="input" type="text" placeholder="Search Products">
                        </p>
                        <p class="control">
                            <a @click="getProducts(1)" class="button is-info">
                            Search
                            </a>
                        </p>
                        <p class="control">
                            <select @change="getProducts(1)" v-model="search.category" class="input">
                                <option disabled selected>Category</option>
                                <option v-for="category in categories" v-bind:key="category.id">{{ category.name }}</option>
                            </select>
                        </p>
                    </div>

                    <div class="columns is-multiline is-scrollable">
                        <div class="column is-3" v-for="product in products" :key="product.id">
                            <div class="card">
                                <div class="card-image">
                                    <!-- <figure class="image is-square"> -->
                                    <img heigth=300 src="../assets/ecommerce-default-product.png" alt="Placeholder image">
                                    <!-- </figure> -->
                                </div>
                                <div class="card-content">
                                    <div class="content">
                                            <p class="title is-6">{{ product.description }}</p>
                                            <p class="subtitle is-6">{{ product.category.name }}</p>
                                            <p class="is-6">TZS {{ product.price }}</p>
                                    </div>
                                </div>
                                <!-- <footer class="card-footer">
                                    <a href="#" class="card-footer-item">Add to Online Catalog</a>
                                    <a href="#" class="card-footer-item">Add Inventory</a>
                                    <a href="#" class="card-footer-item">Delete</a>
                                </footer> -->
                            </div>
                        </div>
                    </div>
                    
                    <nav class="pagination" role="navigation" aria-label="pagination">
                        <a class="button pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getProducts(pages.page-1)">Previous</a>
                        <a class="button pagination-next" :disabled="pages.next==false" @click="getProducts(pages.page+1)">Next page</a>
                    </nav>


                    <!-- <table class="table" v-else>
                        <thead>
                            <tr>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Code</th>
                            <th>Packing</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Cost</th>
                            <th>Created At</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in products" :key="product.id">
                            <td v-if="editing === product.id"><input type="text" v-model="product.category"></td>
                            <td v-else>{{ product.category }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.description"></td>
                            <td v-else>{{ product.description }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.code"></td>
                            <td v-else>{{ product.code }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.packing"></td>
                            <td v-else>{{ product.packing }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.price"></td>
                            <td v-else>{{ product.price }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.quantity"></td>
                            <td v-else>{{ product.quantity }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.cost"></td>
                            <td v-else>{{ product.cost }}</td>
                            <td v-if="editing === product.id"><input type="text" v-model="product.created"></td>
                            <td v-else>{{ product.created }}</td>
                            <td v-if="editing == product.id">
                                <button class="button is-small is-success" @click="editProduct(product)">save</button>
                                <button class="button is-small muted-button" @click="cancelEdit(product)">cancel</button>
                            </td>
                            <td v-else>
                                <button class="button is-small is-primary" @click="editMode(product)">edit</button>
                                <button class="button is-small is-danger" @click="deleteProduct(product.id)">delete</button>
                            </td>
                            </tr>
                        </tbody>
                    </table> -->
                </div>
            </article>
        </div>
    </div>
</template>

<script>
export default {
    name: 'product-table',
    data() {
        return {
            products: [],
            pages: {
                page: null,
                next: null,
                prev: null
            },
            categories: [],
            search: {
                text: '',
                category: ''
            },
            editing: null,
            response: null,
        }
    },
    created() {
        this.getProducts(1)
        this.getCategories()
    },
    methods: {
        getProducts(page) {
            try {
                this.axios.get('http://localhost:5000/products?page='+page+'&search='+this.search.text+'&category='+this.search.category)
                .then(response => {
                    this.products = response.data[0].body
                    // console.log(this.products)
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
        getCategories() {
            this.axios.get('http://localhost:5000/categories')
            .then(response => {
                this.categories = response.data[0]['categories']
            })
            .catch(error => {
                this.response = error
            })
        },
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>