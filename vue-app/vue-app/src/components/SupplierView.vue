<template>
    <div id="product-table">
        
        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div v-else></div>         
        </div>


        <article class="card">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column is-two-fifths">
                        <div class="field is-grouped is-expanding">
                            <div class="control is-expanded">
                                <model-select class="input is-large" ref="search" :options="supplierList" v-model="search" placeholder="search suppliers"></model-select>
                            </div>
                            <div class="control button is-primary" @click="searchSuppliers()">search</div>
                        </div>
                    </div>
                    <div class="column is-two-fifths"></div>
                    <div class="column">
                        <router-link to="/add-supplier" class="button">Add Supplier</router-link>
                    </div>
                </div>
            </div>
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="suppliers && suppliers.length===0">You have no suppliers. Click Add Supplier to add your first supplier.</div>
                <div class="card is-paddingless" v-for="supplier in suppliers" :key="supplier.id" v-else-if="suppliers && suppliers.length > 0">
                    <div class="level">
                        <div class="column has-text-centered"><div class="title is-6 has-text-link">{{ supplier.business_name }}</div></div>
                        <div class="column"><div class="title is-6" v-if="supplier.contact_person"><font-awesome-icon class="font-margin" icon="at" size="lg" /> {{ supplier.contact_person }}</div></div>
                        <div class="column"><div class="title is-6" v-if="supplier.phone"><font-awesome-icon class="font-margin" icon="phone-square-alt" size="lg" />{{ supplier.phone }}</div></div>
                        <div class="column"><div class="title is-6" v-if="supplier.email"><font-awesome-icon class="font-margin" icon="envelope-square" size="lg" />{{ supplier.email }}</div></div>
                        <div class="column">
                            <div class="title is-6" v-if="supplier.plus_code"><font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />{{ supplier.plus_code }}</div>
                            <div class="title is-6" v-else-if="supplier.address"><font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />{{ supplier.address }}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level" role="navigation" aria-label="pagination">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getSuppliers(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getSuppliers(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>

    </div>
</template>

<script>
import { ModelSelect } from 'vue-search-select';
export default {
    name: 'supplier-view',
    components: {
        ModelSelect,
    },
    data() {
        return {
            jwt: '',
            response: null,
            error: null,
            suppliers: null,
            pages: {
                page: null,
                next: null,
                prev: null
            },
            search: null,
            supplierList: [],
        }
    },
    created() {
        this.jwt = this.$store.state.jwt
        this.getSuppliers(1)
        this.getSupplierList()
    },
    methods: {
    getSuppliers(page) {
            this.axios.get('suppliers?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.suppliers = response.data.body
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status == 400) {
                    this.error = "Error while retrieving Suppliers."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        getSupplierList(){
            this.axios.get('suppliers/names', { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.supplierList = response.data.suppliers
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        searchSuppliers(){
            this.axios.get('suppliers/search?supplier='+this.search, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.suppliers = response.data.body
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        closeNotification() {
            this.error = null
        }
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
.font-margin {
    margin: 0px 5px 0px 0px;
}
</style>