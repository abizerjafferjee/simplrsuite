<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">Add to your inventory and track total cost of stock</p>
                <form @submit.prevent="handleSubmit">
                <div class="content">
                    <div v-if="error && submitting">
                        <p class="error-message" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                    </div>
                    <!-- <p v-if="error && submitting" class="error-message">!Please fill out all required fields</p> -->
                    <p v-if="success" class="success-message">Product successfully added</p>

                        <p class="subtitle is-5">Add Inventory</p>

                        <label class="label">* Product</label>
                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <model-select class="input" ref="product" @focus="clearStatus" @keypress="clearStatus" :options="productNames" v-model="procurement.product" placeholder="select item"></model-select>
                            </div>
                            <div class="control"><a class="button" @click="show(2)">Add Product</a></div>
                        </div>
                        <modal name="add-product" :width="800" :height="600"><product-form></product-form></modal>

                        <label class="label">* Quantity</label>
                        <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field is-expanded">
                            <div class="field has-addons">
                                <p class="control"><a class="button is-static">Units</a></p>
                                <p class="control is-expanded">
                                <input class="input" ref="quantity" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.quantity" type="number" placeholder="e.g. 10"/>
                                </p>
                            </div>
                            </div>
                        </div>
                        </div>

                        <p class="subtitle is-5">Add Procurement</p>

                        <label class="label">* Supplier</label>
                        <div class="field is-grouped">
                            <div class="control is-expanded">
                                <model-select class="input" ref="supplier" @focus="clearStatus" @keypress="clearStatus" :options="supplierNames" v-model="procurement.supplier" placeholder="select item"></model-select>
                            </div>
                            <div class="control"><a class="button" @click="show(1)">Add Supplier</a></div>
                        </div>
                        <modal name="add-supplier" :width="800" :height="860"><supplier-form></supplier-form></modal>
                        
                        <label class="label">Invoice Number</label>
                        <input class="input" ref="invoice" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.invoice" type="text" placeholder=""/>

                        <label class="label">* Unit Cost</label>
                        <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field is-expanded">
                            <div class="field has-addons">
                                <p class="control"><a class="button is-static">TZS</a></p>
                                <p class="control is-expanded">
                                    <input class="input" ref="unit_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.unit_cost" type="number" placeholder="e.g. 1000"/>
                                </p>
                            </div>
                            </div>
                        </div>
                        </div>


                        <label class="label">* Total Cost</label>
                        <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field is-expanded">
                            <div class="field has-addons">
                                <p class="control"><a class="button is-static">TZS</a></p>
                                <p class="control is-expanded">
                                    <input class="input" ref="total_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.total_cost" type="number" placeholder="e.g. 50000" />
                                </p>
                            </div>
                            </div>
                            <label class="checkbox"><input type="checkbox" @click="checkbox()">Unit Cost * Quantity</label>
                        </div>
                        </div>

                        <label class="label">Additional Info</label>
                        <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.additional_info"></textarea></div>
                        
                        <button id="submit" class="button is-primary">Add</button>
                    </div>
                </form>
            </article>
        </div>

    </div>
</template>

<script>
import ProductForm from '@/components/ProductForm.vue'
import SupplierForm from '@/components/SupplierForm.vue'
import { ModelSelect } from 'vue-search-select'

export default {
    name: 'procurement-form',
    components: {
        ProductForm,
        SupplierForm,
        ModelSelect
    },
    data() {
        return {
            submitting: false,
            error: false,
            success: false,
            procurement: {
                supplier: null,
                product: null,
                invoice: null,
                quantity: 0,
                unit_cost: 0,
                total_cost: 0,
                additional_info: null
            },
            response: null,
            productNames: [],
            supplierNames: [],
            checked: false,
            errors: []
        }
    },
    created: function() {
        this.getProductNames()
        this.getSupplierNames()
    },
    computed: {
        invalidProduct() {
           if (this.procurement.product === null) {
               this.errors.push({'id':1, 'e':'!Product Name is required.'})
               return true
           }
        },
        invalidSupplier() {
            if (this.procurement.supplier === null) {
                this.errors.push({'id':2, 'e':'!Supplier Name is required.'})
                return true
            }
        }
    },
    methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidSupplier || this.invalidProduct) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addProcurement(this.procurement)
 
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addProcurement(procurement) {
            try {
                this.axios.post('http://localhost:5000/inventory/add', {'body': procurement})
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
            this.$refs.supplier.focus()
        },
        show (form_number) {
            if (form_number === 1) {
                this.$modal.show('add-supplier');
            } else if (form_number === 2) {
                this.$modal.show('add-product');
            }
        },
        clearForm() {
            this.procurement = {
                supplier: null,
                product: null,
                invoice: null,
                quantity: 0,
                unit_cost: 0,
                total_cost: 0
            }
        },
        checkbox () {
            if (this.checked) {
                this.procurement.total_cost = 0
                this.checked = false
            } else {
                this.procurement.total_cost = this.procurement.unit_cost * this.procurement.quantity
                this.checked = true
            }
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
        },
        getSupplierNames() {
            try {
                this.axios.get('http://localhost:5000/suppliers/names')
                .then(response => {
                    this.supplierNames = response.data[0]['suppliers']
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
/* * {
    font-family: 'Open Sans'
} */
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