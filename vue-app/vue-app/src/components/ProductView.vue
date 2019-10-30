<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 class="title level-left">
                                All Products
                            </h1>
                            <div class="level-right">
                                <p class="level-item"><router-link to="/add-product" class="button">Add Product</router-link></p>
                            </div>
                        </div>
                    </div>
                </section>

                <br>

                <div v-if="products && products.length < 1" class="notification">
                    You have no products in your catalog. Click Add Products to add your first product.
                </div>

                <!-- <p v-if="products && products.length < 1" class="empty-table">No Products</p> -->
                <div class="content" v-else>
                    <div class="field is-grouped notification">
                        <p class="control is-expanded">
                            <input v-model="search.text" class="input" type="text" placeholder="Search Products">
                        </p>
                        <p class="control">
                            <select @change="getProducts(1)" v-model="search.category" class="input" placeholder="Category">
                                <!-- <option selected>Category</option> -->
                                <option v-for="category in categories" v-bind:key="category.id">{{ category.name }}</option>
                            </select>
                        </p>
                        <p class="control">
                            <a @click="getProducts(1)" class="button is-info">
                            Search
                            </a>
                        </p>
                    </div>

                    <div class="columns is-multiline is-scrollable">
                        <div class="column is-3" v-for="product in products" :key="product.id">
                            <div class="card">
                                <div class="card-image">
                                    <!-- <figure class="image is-square"> -->
                                    <!-- <img heigth=300 :src="product.image_path" alt="Placeholder image"> -->
                                    <img heigth=300 src="../assets/ecommerce-default-product.png" alt="Placeholder image">
                                    <!-- </figure> -->
                                </div>
                                <div class="card-content">
                                    <div class="content">
                                            <p class="title is-6"><router-link :to="{ path: '/product-detail', query: {productId: product.id}}">{{ product.description }}</router-link></p>
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
            categories: [{'id':0, 'name':''}],
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
                this.categories = this.categories.concat(response.data[0]['categories'])
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