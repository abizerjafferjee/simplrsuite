<template>
    <div id="product-form">

        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link to="/products">Products</router-link></li>
                <li class="is-active">
                    <a aria-current="page">Add Product</a>
                </li>
            </ul>
        </nav>
        
        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div class="title is-6 has-text-success" v-if="success">{{ success }}</div>
            <div v-else></div>         
        </div>

        <article class="card">
            <div class="card-header card-header-title has-background-info has-text-white">Add a Product</div>

            <form class="card-content" @submit.prevent="handleSubmit">

                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">* Category</label>
                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <model-select class="input is-large" ref="search" :options="categories" v-model="product.category" placeholder="select category"></model-select>
                            </div>
                            <div class="control"><a class="button" @click="show">Add Category</a></div>
                        </div>

                        <modal name="add-category"><category-form @add:category="addCategory"></category-form></modal>
                    </div>

                    <div class="column">
                        <label class="label">* Product Title</label>
                        <input class="input" ref="description" @focus="clearStatus" @keypress="clearStatus" v-model="product.description" type="text" placeholder="Cash Book 4Q"/>
                    </div>

                </div>

                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">Auto-Generated SKU</label>
                        <small>A SKU (item number) will be automatically generated. You can also enter another unique identifier below.</small>
                    </div>
                </div>

                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">Code</label>
                        <input class="input" ref="code" @focus="clearStatus" @keypress="clearStatus" v-model="product.code" type="text" placeholder="e.g. H10000M02" />
                    </div>

                    <div class="column">
                        <label class="label">Selling Price</label>
                        <p class="control is-expanded has-icons-left">
                            <input ref="price" @focus="clearStatus" @keypress="clearStatus" v-model="product.price" class="input" type="number" placeholder="5000">
                            <span class="icon is-small is-left">TZS</span>
                        </p>
                    </div>

                    <div class="column">
                        <label class="label">Packing</label>
                        <div class="field has-addons">
                        <p class="control">
                            <span class="select">
                            <select class="button is-primary" ref="packing_type" @focus="clearStatus" @keypress="clearStatus" v-model="product.packing_type" type="text">
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
                    </div>
                </div>
                
                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">Product Image</label>
                        <div class="file has-name is-fullwidth">
                            <label class="file-label">
                                <input class="file-input" type="file" name="file" ref="file" @focus="clearStatus" @keypress="clearStatus" v-on:change="handleFile()">
                                <span class="file-cta">
                                    <span class="file-label">Choose a file…</span>
                                </span>
                                <span class="file-name" v-if="product_file">{{ product_file.name }}</span>
                                <span class="file-name" v-else>image.png</span>
                            </label>
                        </div>  
                    </div>
                </div>

                <div class="columns is-paddingless">
                    <div class="column">
                        <label class="label">Additional Info</label>
                        <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="product.additional_info" placeholder="e.g. Product description, dimensions, weight and colors."></textarea></div>                 
                    </div>
                </div>

                <button id="submit" class="button is-primary">Add Product</button>
            </form>
        </article>

    </div>
</template>

<script>
import CategoryForm from '@/components/CategoryForm.vue'
import { ModelSelect } from 'vue-search-select';
export default {
   name: 'product-form',
   components: {
       CategoryForm,
       ModelSelect
   },
   data() {
       return {
           jwt: '',
           response: null,
           success: null,
           error: null,
           product: {
               category: null,
               description: null,
               packing_type: "Piece",
               packing: null,
               code: null,
               currency: "TZS",
               price: null,
               additional_info: null,
           },
           product_file: null,
           categories: [],
       }
   },
   created: function() {
       this.jwt = this.$store.state.jwt
       this.getCategories()
   },
   methods: {
        handleSubmit() {
            this.clearStatus()
            this.addProduct()
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addProduct() {
            let formData = new FormData()
            formData.append('file', this.product_file)
            formData.append('body', JSON.stringify(this.product))
            
            this.axios.post('products', formData, { headers: {'Content-Type': 'multipart/form-data', 'Authorization': `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Product added."
                this.clearForm()
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status == 400) {
                    this.error = error.response.data['message']
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        clearForm() {
            this.product = {
               category: null,
               description: null,
               packing_type: "Piece",
               packing: null,
               code: null,
               currency: "TZS",
               price: null,
               additional_info: null,
           }
        },
        makeCategoryList(categories) {
            var categoryList = []
            for (var i=0; i < categories.length; i++) {
                categoryList.push({
                    'value':categories[i]['id'],
                    'text':categories[i]['name']
                })
            }
            return categoryList
        },
        getCategories() {
            this.axios.get('categories', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.categories = this.makeCategoryList(response.data['categories'])
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        addCategory(category) {
            this.hide()
            this.axios.post('categories', {'body': category}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Category added."
                this.getCategories()
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status == 400) {
                    this.error = error.response.data['message']
                } else {
                    this.error = "Internal Server Error"
                }
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