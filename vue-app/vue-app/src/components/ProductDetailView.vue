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

                <nav class="level">
                    <div class="level-left">
                        <p class="title">{{ product.description }}</p>
                    </div>
                    <div class="level-right">
                    </div>
                </nav>

                <div class="content">
                    <a class="button is-small">Edit Product</a>
                    <a class="button is-small">Delete Product</a>
                    <a class="button is-small">Remove Inventory</a>
                    <a class="button is-small">Remove All Inventory</a>
                    <p>Who are the suppliers of this product? (last 10 suppliers)</p>
                    <p>What is the total payment due for this product?</p>
                    <p>What is the total cost of inventory for this product?</p>
                    <p>What is the total expected revenue from this product?</p>
                    <p>What is the frequency of procurement for this product?</p>
                </div>

            </article>
        </div>
    </div>
</template>

<script>
export default {
    name: 'product-detail',
    data() {
        return {
            productId: null,
            product: null,
            response: null
        }
    },
    mounted() {
        if (this.$route.query.productId) {
            this.productId = this.$route.query.productId
            this.getProduct()
        }
    },
    methods: {
        getProduct() {
            try {
                this.axios.get('http://localhost:5000/products/'+this.productId)
                .then(response => {
                    this.product = response.data[0].body
                })
                .catch(e => {
                    this.response = e
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