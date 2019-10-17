<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <nav class="breadcrumb" aria-label="breadcrumbs">
                <ul>
                    <li><router-link to="/suppliers">Suppliers</router-link></li>
                    <li class="is-active">
                        <a href="#" aria-current="page">Supplier Details</a>
                    </li>
                </ul>
                </nav>

                <nav class="level">
                    <div class="level-left">
                        <p class="title">{{ supplier.business_name }}</p>
                    </div>
                    <div class="level-right">
                    </div>
                </nav>

                <div class="content">
                    <a class="button is-small">Edit Supplier</a>
                    <a class="button is-small">Delete Supplier</a>
                    <a class="button is-small">Pay a invoice or procurement</a>
                    <p>All outstanding invoices for supplier</p>
                    <p>All paid invoices for supplier</p>
                    <p>All paid/ non-paid procurements from supplier without invoice</p>
                    <p>Total value of goods from supplier and rank of supplier</p>
                    <p>Frequency of procurements from supplier</p>
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
            supplierId: null,
            supplier: null,
            response: null
        }
    },
    created() {
        if (this.$route.query.supplierId) {
            this.supplierId = this.$route.query.supplierId
            this.getSupplier()
        }
    },
    methods: {
        getSupplier() {
            try {
                this.axios.get('http://localhost:5000/suppliers/'+this.supplierId)
                .then(response => {
                    this.supplier = response.data[0].body
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