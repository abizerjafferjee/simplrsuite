<template>
    <div id="product-table">

        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div v-else></div>
        </div>

        <article class="card has-text-centered">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column is-three-fifths">
                        <div class="field is-grouped is-expanding">
                            <div class="control is-expanded">
                                <model-select class="input is-large" ref="search" :options="productNames" v-model="productSearch" placeholder="search products"></model-select>
                            </div>
                            <div class="control button is-primary" @click="searchProducts()">search</div>
                        </div>
                    </div>
                    <div class="column"></div>
                    <div class="column">
                        <router-link to="/add-product" class="button">Add Product</router-link>
                    </div>
                </div>
            </div>
            <div class="card card-content has-background-light" style="min-height:500px">
                <div class="notification" v-if="products && products.length===0">You have no products in your catalog. Click Add Products to add your first product.</div>
                <div class="columns is-multiline is-scrollable" v-else>
                    <div class="column is-4" v-for="product in products" :key="product.id">
                        <div class="card">
                            <div class="card-image">
                                <img height=200 width=200 :src="require('../assets/uploads/' + product.image_path)" v-if="product.image_path">
                                <img heigth=200 width=200 src="../assets/ecommerce-default-product.png" alt="Placeholder image" v-else>
                            </div>
                            <div class="card-content is-size-6 has-text-grey">
                                <!-- <div class="content"> -->
                                        <p class="title is-6"><router-link :to="{ path: '/product-detail', query: {productId: product.id}}">{{ product.description }}</router-link></p>
                                        <p>{{ product.category.name }}</p>
                                        <p>{{ product.currency }} {{ product.price | currency }}</p>
                                <!-- </div> -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getProducts(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getProducts(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>

    </div>
</template>

<script>
var numeral = require("numeral");
import moment from 'moment'
import { ModelSelect } from 'vue-search-select';
export default {
    name: 'product-table',
    components: {
        ModelSelect,
    },
    data() {
        return {
            products: null,
            pages: {
                page: null,
                next: null,
                prev: null
            },
            productNames: [],
            productSearch: null,
            response: null,
            error: null,
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
        this.getProductNames()
    },
    methods: {
        getProducts(page) {
            this.axios.get('products?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.products = response.data.body
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        searchProducts() {
            this.axios.get('products/search?product='+this.productSearch, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.products = response.data.body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        getProductNames() {
            this.axios.get('products/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.productNames = response.data.body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
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