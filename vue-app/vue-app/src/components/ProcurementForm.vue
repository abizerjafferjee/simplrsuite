<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">Add Inventory</p>
                <p class="subtitle">Add to your inventory and track total cost of stock.</p>
                <div class="content">
                    <form @submit.prevent="handleSubmit">

                        <label class="label">Product</label>

                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <model-select class="input" ref="product" @focus="clearStatus" @keypress="clearStatus" :options="productNames" v-model="procurement.product" placeholder="select item"></model-select>
                            </div>
                            <div class="control"><a class="button" @click="show">Add Product</a></div>
                        </div>
                        <!-- <input class="input" ref="product" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.product" type="text" placeholder="search products..."/> -->

                        <modal name="add-procurement" :width="800" :height="600"><product-form></product-form></modal>
                        
                        <label class="label">Unit Cost</label>
                        <input class="input" ref="unit_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.unit_cost" type="text" placeholder="cash book 4q"/>

                        <label class="label">Quantity</label>
                        <input class="input" ref="quantity" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.quantity" type="text" placeholder="e.g. 10 pieces per pack"/>

                        <label class="label">Total Cost</label>
                        <input class="input" ref="total_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.total_cost" type="text" placeholder="e.g. AB-250" />
                        
                        <p v-if="error && submitting" class="error-message">!Please fill out all required fields</p>
                        <p v-if="success" class="success-message">Product successfully added</p>
                        
                        <button id="submit" class="button is-primary">Add to Inventory</button>
                    </form>
                </div>
            </article>
        </div>

    </div>
</template>

<script>
import ProductForm from '@/components/ProductForm.vue'
import { ModelSelect } from 'vue-search-select'

export default {
    name: 'procurement-form',
    components: {
        ProductForm,
        ModelSelect
    },
    data() {
        return {
            submitting: false,
            error: false,
            success: false,
            procurement: {
                product: null,
                quantity: null,
                unit_cost: null,
                total_cost: null
            },
            response: null,
            productNames: [],
        }
    },
    created: function() {
        this.getProductNames()
    },
    computed: {
    },
    methods: {
        handleSubmit() {
            this.submitting = true
            this.clearStatus()
            this.addProcurement(this.procurement)
            this.error = false
            this.success = true
            this.submitting = false
            this.$refs.category.focus()
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addProcurement(product) {
            try {
                this.axios.post('http://localhost:5000/products/add', {'body': product})
                .then(response => {
                    var newProduct = response.data[0]['body']
                    this.products.push(newProduct)
                })
                .catch(e => {
                    this.response = e
                })
            } catch (error) {
                this.response = error
            }
        },
        show () {
           this.$modal.show('add-procurement');
        },
        getProductNames() {
            try {
                this.axios.get('http://localhost:5000/products/names')
                .then(response => {
                    this.productNames = response.data[0]['products']
                })
                .catch(e => {
                    this.response = e
                })

            } catch (error) {
                this.response = error
            }
        }
    }
}
</script>

<style scoped>
#submit {
    align-self: center
}
form {
    margin-bottom: 2rem;
}
[class*='-message'] {
    font-weight: 500;
}
.error-message {
    color: #d33c40;
}

.success-message {
    color: #32a95d;
}
</style>