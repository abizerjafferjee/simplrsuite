<template>
    <div id="product-table">
        
        <div class="section notification" v-if="error">
            <button @click="closeNotification" class="delete"></button>
            {{ error }}
        </div>

        <section class="welcome card card-content has-background-light">
            <div class="columns">
                <div class="column is-two-fifths">
                    <div class="field is-grouped is-expanding">
                        <div class="control is-expanded">
                            <model-select class="input is-large" ref="search" :options="supplierList" v-model="search" placeholder="search suppliers"></model-select>
                        </div>
                        <div class="control button is-primary">search</div>
                    </div>
                </div>
                <div class="column is-two-fifths"></div>
                <div class="column">
                    <router-link to="/add-supplier" class="button">Add Supplier</router-link>
                </div>
            </div>
        </section>


        
        
        <div v-if="suppliers && suppliers.length < 1" class="notification">
            You have no suppliers. Click Add Supplier to add your first supplier.
        </div>

        <div class="section" v-else>
            <div v-for="supplier in suppliers" :key="supplier.id">
                <div class="card card-content" style="margin:0px 0px 10px 0px">
                    <article class="media">
                        <div class="media-content">
                            <div class="content">
                                <p class="title is-4 has-text-link">
                                    {{ supplier.business_name }}
                                </p>
                            </div>
                            <div class="level is-mobile">
                                <div class="level-left is-size-6 has-text-grey">
                                    <p class="level-item" aria-label="transactions" v-if="supplier.contact_person">
                                        <font-awesome-icon class="font-margin" icon="at" size="lg" /> {{ supplier.contact_person }}
                                    </p>
                                    <p class="level-item" aria-label="transactions" v-if="supplier.email">
                                        <font-awesome-icon class="font-margin" icon="envelope-square" size="lg" /> <a>{{ supplier.email }}</a>
                                    </p>
                                    <p class="level-item" aria-label="transactions" v-if="supplier.phone">
                                        <font-awesome-icon class="font-margin" icon="phone-square-alt" size="lg" />{{ supplier.phone }}
                                    </p>
                                </div>
                            </div>
                            <div class="level is-mobile">
                                <div class="level-left is-size-6 has-text-grey">
                                    <p class="level-item" aria-label="transactions" v-if="supplier.address">
                                        <font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />{{ supplier.address }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </article>
                </div>
            </div>
        </div>

        <div class="section" v-if="suppliers.length > 0">
            <nav class="pagination" role="navigation" aria-label="pagination">
                <a class="button pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getSuppliers(pages.page-1)">Previous</a>
                <a class="button pagination-next" :disabled="pages.next==false" @click="getSuppliers(pages.page+1)">Next page</a>
            </nav>
        </div>

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
            suppliers: [],
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
            .catch(e => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
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
            .catch(e => {
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