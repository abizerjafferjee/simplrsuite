<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">All Product</p>
                <p class="subtitle">View products, costs, quantities and prices.</p>
                
                <p v-if="products.length < 1" class="empty-table">No Products</p>
                <div class="content" v-else>
                    <div class="columns is-multiline">
                        <div class="column is-4" v-for="product in products" :key="product.id">
                            <div class="card">
                                <div class="card-image">
                                    <figure class="image is-4by3">
                                    <img src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image">
                                    </figure>
                                </div>
                                <div class="card-content">
                                    <div class="media">
                                        <div class="media-left">
                                            <p class="title is-4">{{ product.description }}</p>
                                            <p class="subtitle is-6">{{ product.category.name }}</p>
                                        </div>
                                        <div class="media-content">
                                        </div>
                                    </div>

                                    <div class="content"></div>
                                </div>
                                <!-- <footer class="card-footer">
                                    <a href="#" class="card-footer-item">Save</a>
                                    <a href="#" class="card-footer-item">Edit</a>
                                    <a href="#" class="card-footer-item">Delete</a>
                                </footer> -->
                            </div>
                        </div>
                    </div>


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
            editing: null,
            response: null,
        }
    },
    mounted() {
        this.getProducts(1)
    },
    methods: {
        getProducts(page) {
            try {
                this.axios.get('http://localhost:5000/products?='+page)
                .then(response => {
                    this.products = response.data[0].body
                    console.log(this.products)
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
        }
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>