<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                    <ul>
                        <li><router-link to="/products">Products</router-link></li>
                        <li class="is-active">
                            <a aria-current="page">Add Product</a>
                        </li>
                    </ul>
                </nav>

                <section class="hero welcome is-small has-background-light">
                    <div class="hero-body">
                        <div class="container">
                            <p class="title">Add Product</p>
                            <p class="subtitle">Add your product information, image and price and we'll add it to your catalog.</p>
                        </div>
                    </div>
                </section>
                
                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>
                
                <section>
                    <div class="content">

                        <div v-if="error && submitting">
                            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                        </div>
                        <p v-if="success" class="notification is-success">Product successfully added</p>

                        <form @submit.prevent="handleSubmit">

                            <label class="label">* Category</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <select class="input" ref="category" @focus="clearStatus" @keypress="clearStatus" v-model="product.category" type="text">
                                        <option v-for="category in categories" v-bind:key="category.id">{{ category.name }}</option>
                                    </select>
                                </div>
                                <div class="control"><a class="button" @click="show">Add Category</a></div>
                            </div>

                            <modal name="add-category"><category-form @add:category="addCategory"></category-form></modal>

                            <label class="label">* Product Title</label>
                            <input class="input" ref="description" @focus="clearStatus" @keypress="clearStatus" v-model="product.description" type="text" placeholder="Cash Book 4Q"/>
                            
                            <label class="checkbox">
                            <input type="checkbox" @click="codeCheckBox()">
                                A SKU (item number) will be automatically generated for you. You can choose to enter another unique identifier below.
                            </label>
                            
                            <label class="label">Code</label>
                            <input class="input" ref="code" @focus="clearStatus" @keypress="clearStatus" v-model="product.code" type="text" :disabled="enterCode === true" placeholder="e.g. H10000M02" />

                            <label class="label">Product Type</label>
                            <div class="field">
                                <select class="input" ref="product_type" @focus="clearStatus" @keypress="clearStatus" v-model="product.product_type" type="text">
                                    <option>Finished Good</option>
                                    <option>Raw Material</option>
                                </select>
                            </div>

                            <label class="label">Product Image</label>
                            <div class="file has-name is-fullwidth">
                                <label class="file-label">
                                    <input class="file-input" type="file" name="file" ref="file" @focus="clearStatus" @keypress="clearStatus" v-on:change="handleFile()">
                                    <span class="file-cta">
                                        <span class="file-icon"><i class="fas fa-upload"></i></span>
                                        <span class="file-label">Choose a file…</span>
                                    </span>
                                    <span class="file-name" v-if="product_file">{{ product_file.name }}</span>
                                    <span class="file-name" v-else>image.png</span>
                                </label>
                            </div>

                            <label class="label">Packing</label>
                            <div class="field has-addons">
                            <p class="control">
                                <span class="select">
                                <select class="button is-light" ref="packing_type" @focus="clearStatus" @keypress="clearStatus" v-model="product.packing_type" type="text">
                                    <option>Piece</option>
                                    <option>Dozen</option>
                                    <option>Carton</option>
                                    <option>Pack</option>
                                    <option>Pallet</option>
                                    <option>Custom</option>
                                </select>
                                </span>
                            </p>
                            <p class="control is-expanded">
                                <input class="input" ref="packing" @focus="clearStatus" @keypress="clearStatus" v-model="product.packing" type="text" placeholder="e.g. 10 pieces per pack"/>
                            </p>
                            </div>

                            <label class="label">Selling Price</label>
                            <div class="field has-addons">
                            <p class="control">
                                <span class="select">
                                <select class="button is-light" ref="currency" @focus="clearStatus" @keypress="clearStatus" v-model="product.currency" type="text">
                                    <option>TZS</option>
                                    <option>KES</option>
                                    <option>USD</option>
                                    <option>RMB</option>
                                    <option>AED</option>
                                </select>
                                </span>
                            </p>
                            <p class="control is-expanded">
                                <input ref="price" @focus="clearStatus" @keypress="clearStatus" v-model="product.price" class="input" type="number" placeholder="5000">
                            </p>
                            </div>

                            <label class="label">Additional Info</label>
                            <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="product.additional_info" placeholder="e.g. Product description, dimensions, weight and colors."></textarea></div>
                            
                            <button id="submit" class="button is-primary">Add Product</button>
                        </form>
                    </div>
                </section>
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
               packing_type: "Piece",
               packing: null,
               code: null,
               currency: "TZS",
               price: null,
               additional_info: null,
           },
           product_file: null,
           categories: [],
           response: null,
           enterCode: true,
           errors: [],
           errorNotification: null,
           jwt: ''
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getCategories()
   },
   computed: {
        // invalidProduct() {
        //    return this.product.description === null
        // }
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidProduct() || this.invalidCategory()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addProduct()
        },
        clearStatus() {
            this.error = false
            this.success = false
            this.errors = []
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
        addProduct() { 
            try {
                let formData = new FormData()
                formData.append('file', this.product_file)
                formData.append('body', JSON.stringify(this.product))
                
                this.axios.post('products', formData, { headers: {'Content-Type': 'multipart/form-data', 'Authorization': `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.showSuccess()
                    }
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
               packing_type: "Piece",
               packing: null,
               code: null,
               currency: "TZS",
               price: null,
               additional_info: null,
           }
        },
        getCategories() {
                this.axios.get('categories', { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.categories = response.data[0]['categories']
                    }
                })
                .catch(error => {
                    this.response = error
                    this.errorNotification = "Internal Server Error."
                })
        },
        show () {
           this.$modal.show('add-category');
        },
        hide () {
            this.$modal.hide('add-category');
        },
        handleFile() {
            this.product_file = this.$refs.file.files[0];
        },
        codeCheckBox () {
            this.enterCode = !this.enterCode
            if (this.enterCode === false) {
                this.product.code = null
            }
        },
        addCategory(category) {
            try {
                this.hide()
                this.axios.post('categories', {'body': category}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        var newCategory = response.data[0]['category']
                        this.categories.push(newCategory)
                    }
                })
                .catch(e => {
                    this.response = e
                    this.errorNotification = "Internal Server Error: add category."
                })
            } catch (error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
        },
        invalidProduct() {
            if (this.product.description === null) {
                this.errors.push({'id':1, 'e':'!Product title is empty.'})
                return true
            } else if (this.product.description.length < 3) {
                this.errors.push({'id': 2, 'e':'!Product title should be at least 3 characters long.'})
                return true
            }
            return false
        },
        invalidCategory() {
            if (this.product.category === null) {
                this.errors.push({'id':3, 'e':'!Product category is empty.'})
                return true
            }
            return false
        },
        closeNotification() {
            this.errorNotification = null
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