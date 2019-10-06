<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">Add Product</p>
                <p class="subtitle">Add products, costs, quantities and prices. This will be added to your catalog.</p>
                <div class="content">
                    <p v-if="error && submitting" class="error-message">!Please fill out all required fields</p>
                    <p v-if="success" class="success-message">Product successfully added</p>
                    <form @submit.prevent="handleSubmit">

                        <label class="label">Category</label>
                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <select class="select" ref="category" @focus="clearStatus" @keypress="clearStatus" v-model="product.category" type="text">
                                    <option v-for="category in categories" v-bind:key="category.id">{{ category.name }}</option>
                                </select>
                            </div>
                            <div class="control"><a class="button" @click="show">Add Category</a></div>
                        </div>

                        <modal name="add-category"><category-form @add:category="addCategory"></category-form></modal>
                        
                        <label class="label">Product (Label/ Description)</label>
                        <input class="input" ref="description" @focus="clearStatus" @keypress="clearStatus" v-model="product.description" type="text" placeholder="cash book 4q"/>

                        <label class="label">Packing</label>
                        <input class="input" ref="packing" @focus="clearStatus" @keypress="clearStatus" v-model="product.packing" type="text" placeholder="e.g. 10 pieces per pack"/>

                        <label class="label">Code</label>
                        <input class="input" ref="code" @focus="clearStatus" @keypress="clearStatus" v-model="product.code" type="text" placeholder="e.g. AB-250" />
                        
                        <label class="label">Selling Price</label>
                        <input class="input" ref="price" @focus="clearStatus" @keypress="clearStatus" v-model="product.price" type="number" />

                        
                        <button id="submit" class="button is-primary">Add Product</button>
                    </form>
                </div>
            </article>
        </div>

    </div>
</template>

<script>
import CategoryForm from '@/components/CategoryForm.vue'

export default {
   name: 'product-form',
   components: {
       CategoryForm
   },
   data() {
       return {
           submitting: false,
           error: false,
           success: false,
           product: {
               category: null,
               description: null,
               product_type: null,
               packing: null,
               code: null,
               price: null
           },
           categories: [],
           response: null
       }
   },
   created: function() {
       this.getCategories()
   },
   computed: {
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            this.clearStatus()
            this.addProduct(this.product)
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        showError() {
            this.error = true
            this.submitting = true
            this.success = false
        },
        showSuccess() {
            this.error = false
            this.submitting = false
            this.success = true
            this.clearForm()
            // this.$refs.category.focus()
        },
        addProduct(product) {
            try {
                this.axios.post('http://localhost:5000/products/add', {'body': product})
                .then(response => {
                    this.response = response
                    this.showSuccess()
                })
                .catch(e => {
                    this.response = e
                    this.showError()
                })
            } catch (error) {
                this.response = error
                this.showError()
            }
        },
        clearForm() {
            this.product = {
               category: null,
               description: null,
               product_type: null,
               packing: null,
               code: null,
               price: null
           }
        },
        getCategories() {
                this.axios.get('http://localhost:5000/categories')
                .then(response => {
                    this.categories = response.data[0]['categories']
                    console.log(this.categories)
                })
                .catch(error => {
                    this.response = error
                })
        },
        show () {
           this.$modal.show('add-category');
        },
        addCategory(category) {
            try {
                this.axios.post('http://localhost:5000/categories/add', {'body': category})
                .then(response => {
                    var newCategory = response.data[0]['category']
                    this.categories.push(newCategory)
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