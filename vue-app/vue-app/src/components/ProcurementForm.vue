<template>
    <div id="product-form">

        <div class="tile is-parent">
            <article class="tile is-child">
                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/inventory">Inventory</router-link></li>
                    <li class="is-active">
                        <a aria-current="page">Add Inventory</a>
                    </li>
                </ul>
                </nav>

                <section class="hero welcome is-small has-background-light">
                    <div class="hero-body">
                        <div class="container">
                            <p class="title">Adds to your inventory, tracks invoices and payments</p>
                        </div>
                    </div>
                </section>

                <br>

                <section>
                    <div class="content">
                        <div v-if="error && submitting">
                            <p class="notification is-danger" v-for="e in errors" v-bind:key="e.id">{{ e.e }}</p>
                        </div>
                        <p v-if="success" class="notification is-success">Successfully added to Inventory</p>
                        
                        <br>
                        <form @submit.prevent="handleSubmit">

                            <p class="title is-size-4">Add Inventory</p>

                            <label class="label">* Product</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="product" @focus="clearStatus" @keypress="clearStatus" :options="productNames" v-model="procurement.product" placeholder="select item"></model-select>
                                </div>
                                <div class="control"><router-link to="/add-product" class="button">Add Product</router-link></div>
                            </div>

                            <label class="label">* Quantity</label>
                            <div class="field is-horizontal">
                                <div class="field-body">
                                    <div class="field is-expanded">
                                    <div class="field has-addons">
                                        <p class="control"><a class="button is-light">Units</a></p>
                                        <p class="control is-expanded">
                                        <input class="input" ref="quantity" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.quantity" type="number" placeholder="e.g. 10"/>
                                        </p>
                                    </div>
                                    </div>
                                </div>
                            </div>

                            <p class="title is-size-4">Record Procurement</p>

                            <label class="label">* Supplier</label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <model-select class="input" ref="supplier" @focus="clearStatus" @keypress="clearStatus" :options="supplierNames" v-model="procurement.supplier" placeholder="select item"></model-select>
                                </div>
                                <div class="control"><router-link to="/add-supplier" class="button">Add Supplier</router-link></div>
                                
                            </div>
                            
                            <label class="label">Location</label>
                            <input class="input" ref="location" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.location" type="text" placeholder="e.g. Shop or Warehouse"/>

                            <label class="label">Invoice Number</label>
                            <input class="input" ref="invoice" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.invoice" type="text" placeholder=""/>

                            <label class="label">* Unit Cost</label>
                            <div class="field has-addons">
                                <p class="control">
                                    <span class="select">
                                    <select class="button is-light" ref="currency" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.currency" type="text">
                                        <option>TZS</option>
                                        <option>KES</option>
                                        <option>USD</option>
                                        <option>RMB</option>
                                        <option>AED</option>
                                    </select>
                                    </span>
                                </p>
                                <p class="control is-expanded">
                                    <input class="input" ref="unit_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.unit_cost" type="number" placeholder="e.g. 1000"/>
                                </p>
                            </div>

                            <label class="label">* Total Cost</label>
                            <div class="field has-addons">
                                <p class="control">
                                    <span class="select">
                                    <select class="button is-light" ref="currency" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.currency" type="text">
                                        <option>TZS</option>
                                        <option>KES</option>
                                        <option>USD</option>
                                        <option>RMB</option>
                                        <option>AED</option>
                                    </select>
                                    </span>
                                </p>
                                <p class="control is-expanded">
                                    <input class="input" ref="total_cost" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.total_cost" type="number" placeholder="e.g. 50000" />
                                </p>
                                <p class="control">
                                    <label class="checkbox"><input type="checkbox" @click="checkbox()">Unit Cost * Quantity</label>
                                </p>
                            </div>

                            <label class="label">* Paid</label>
                            <div class="field is-horizontal">
                                <select class="input" ref="paid" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.paid" type="text">
                                    <option>Paid</option>
                                    <option>Unpaid</option>
                                </select>
                            </div>

                            <label class="label">Additional Info</label>
                            <div class="field"><textarea class="textarea" ref="additional_info" @focus="clearStatus" @keypress="clearStatus" v-model="procurement.additional_info" placeholder="e.g. Delivery note number for reference, note of damage to goods etc"></textarea></div>
                            
                            <button id="submit" class="button is-primary">Add</button>
                        </form>
                    </div>
                </section>

            </article>
        </div>

    </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select'

export default {
    name: 'procurement-form',
    components: {
        // ProductForm,
        // SupplierForm,
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
                location: null,
                invoice: null,
                quantity: 0,
                currency: "TZS",
                unit_cost: 0,
                total_cost: 0,
                paid: 'Paid',
                additional_info: null
            },
            response: null,
            productNames: [],
            supplierNames: [],
            checked: false,
            errors: [],
        }
    },
    created: function() {
        this.getProductNames()
        this.getSupplierNames()
    },
    computed: {
        // packingUnit() {
        //     return this.getPackingUnit()
        // }
    },
    methods: {
        handleSubmit() {
            this.submitting = true
            if (this.invalidSupplier() || this.invalidProduct()) {
                this.showError()
                return
            }
            this.clearStatus()
            this.addProcurement()
 
        },
        clearStatus() {
            this.error = false
            this.success = false
        },
        addProcurement() {
            try {
                this.axios.post('http://localhost:5000/inventory', {'body': this.procurement})
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
            // this.$refs.supplier.focus()
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
                location: null,
                invoice: null,
                quantity: 0,
                currency: "TZS",
                unit_cost: 0,
                total_cost: 0,
                paid: 'Paid',
                additional_info: null
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
        },
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
        },
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