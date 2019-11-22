<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero welcome is-small has-background-light">
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

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>
                <br>

                <div v-if="products && products.length < 1" class="notification">
                    You have no products in your catalog. Click Add Products to add your first product.
                </div>

                <div class="content" v-else>
                    <div class="field is-grouped notification">
                        <p class="control is-expanded">
                            <input v-model="search.text" class="input" type="text" placeholder="Search Products">
                        </p>
                        <p class="control">
                            <select @change="getProducts(1)" v-model="search.category" class="input" placeholder="Category">
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
                                    <img :src="require('../assets/uploads/' + product.image_path)" v-if="product.image_path">
                                    <img heigth=300 src="../assets/ecommerce-default-product.png" alt="Placeholder image" v-else>
                                </div>
                                <div class="card-content is-size-6 has-text-grey">
                                    <div class="content">
                                            <p class="subtitle"><router-link :to="{ path: '/product-detail', query: {productId: product.id}}">{{ product.description }}</router-link></p>
                                            <p>{{ product.category.name }}</p>
                                            <p>{{ product.currency }} {{ product.price | currency }}</p>
                                    </div>
                                </div>
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
var numeral = require("numeral");
import moment from 'moment'
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
        this.getProducts(1)
        this.getCategories()
    },
    methods: {
        getProducts(page) {
            try {
                this.axios.get('products?page='+page+'&search='+this.search.text+'&category='+this.search.category, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.products = response.data[0].body
                        this.pages.page = response.data[0].page
                        this.pages.next = response.data[0].next
                        this.pages.prev = response.data[0].prev
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
        getCategories() {
            try {
                this.axios.get('categories', { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.categories = this.categories.concat(response.data[0]['categories'])
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
        },
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>