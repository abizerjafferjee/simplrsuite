<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">Add Product</p>
                <p class="subtitle">Add products, costs, quantities and prices. This will be added to your catalog.</p>
                <div class="content">
                    <p v-if="error && submitting" class="error-message">!Please fill out all fields with an asterisk (*).</p>
                    <p v-if="success" class="success-message">Product successfully added</p>
                    <form @submit.prevent="handleSubmit">

                        <label class="label">Category</label>
                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <select class="input" ref="category" @focus="clearStatus" @keypress="clearStatus" v-model="product.category" type="text">
                                    <option v-for="category in categories" v-bind:key="category.id">{{ category.name }}</option>
                                </select>
                            </div>
                            <div class="control"><a class="button" @click="show">Add Category</a></div>
                        </div>

                        <modal name="add-category"><category-form @add:category="addCategory"></category-form></modal>
                        
                        <label class="label">* Product (Label/ Description)</label>
                        <input class="input" ref="description" @focus="clearStatus" @keypress="clearStatus" v-model="product.description" type="text" placeholder="cash book 4q"/>
                        
                        <label class="label">Upload Image of Product</label>
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
                        <input class="input" ref="packing" @focus="clearStatus" @keypress="clearStatus" v-model="product.packing" type="text" placeholder="e.g. 10 pieces per pack"/>

                        <label class="label">Code</label>
                        <input class="input" ref="code" @focus="clearStatus" @keypress="clearStatus" v-model="product.code" type="text" placeholder="e.g. AB-250" />
                        
                        <label class="label">Selling Price</label>
                        <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field is-expanded">
                            <div class="field has-addons">
                                <p class="control"><a class="button is-static">TZS</a></p>
                                <p class="control is-expanded">
                                <input ref="price" @focus="clearStatus" @keypress="clearStatus" v-model="product.price" class="input" type="number" placeholder="5000">
                                </p>
                            </div>
                            </div>
                        </div>
                        </div>

                        <label class="label">Additional Info</label>
                        <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="product.additional_info"></textarea></div>
                        
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
               price: null,
               additional_info: null,
           },
           product_file: null,
           categories: [],
           response: null
       }
   },
   created: function() {
       this.getCategories()
   },
   computed: {
        invalidProduct() {
           return this.product.description === null
        }
   },
   methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidProduct) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addProduct()
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
        addProduct() { 
            try {
                let formData = new FormData()
                formData.append('file', this.product_file)
                formData.append('body', JSON.stringify(this.product))
                
                this.axios.post('http://localhost:5000/products/add', formData, { headers: {'Content-Type': 'multipart/form-data'}})
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
                })
                .catch(error => {
                    this.response = error
                })
        },
        show () {
           this.$modal.show('add-category');
        },
        handleFile() {
            this.product_file = this.$refs.file.files[0];
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