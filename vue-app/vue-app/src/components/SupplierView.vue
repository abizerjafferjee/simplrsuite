<template>
    <div id="product-table">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 class="title level-left">
                                All Suppliers
                            </h1>
                            <div class="level-right">
                                <p class="level-item"><router-link to="/add-supplier" class="button">Add Supplier</router-link></p>
                            </div>
                        </div>
                    </div>
                </section>

                <div class="notification" v-if="error">
                    <button @click="closeNotification" class="delete"></button>
                    {{ error }}
                </div>
                <br>
                
                <div v-if="suppliers && suppliers.length < 1" class="notification">
                    You have no suppliers. Click Add Supplier to add your first supplier.
                </div>

                <div class="content" v-else>
                    <div class="field is-grouped notification">
                        <p class="control is-expanded">
                            <input v-model="search.text" class="input" type="text" placeholder="Search Suppliers">
                        </p>
                        <p class="control">
                            <a @click="getSuppliers(1)" class="button is-info">
                            Search
                            </a>
                        </p>
                    </div>

                    <div v-for="supplier in suppliers" :key="supplier.id">
                        <div class="box" style="margin:0px 0px 10px 0px">
                            <article class="media">
                                <div class="media-content">
                                    <div class="content">
                                        <p class="title is-3 has-text-link">
                                            {{ supplier.business_name }}
                                        </p>
                                    </div>
                                    <div class="level is-mobile">
                                        <div class="level-left is-size-5 has-text-grey">
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
                                        <div class="level-left is-size-5 has-text-grey">
                                            <p class="level-item" aria-label="transactions" v-if="supplier.address">
                                                <font-awesome-icon class="font-margin" icon="map-marker-alt" size="lg" />{{ supplier.address }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </article>
                        </div>
                    </div>

                    <br>
                    <nav class="pagination" role="navigation" aria-label="pagination">
                        <a class="button pagination-previous" title="This is the first page" :disabled="pages.prev==false" @click="getSuppliers(pages.page-1)">Previous</a>
                        <a class="button pagination-next" :disabled="pages.next==false" @click="getSuppliers(pages.page+1)">Next page</a>
                    </nav>
                </div>
            </article>
        </div>
    </div>
</template>

<script>

export default {
    name: 'supplier-view',
    components: {
    },
    data() {
        return {
            suppliers: [],
            pages: {
                page: null,
                next: null,
                prev: null
            },
            search: {
                text: ''
            },
            editing: null,
            response: null,
            error: null,
            jwt: ''
        }
    },
    created() {
        this.jwt = this.$store.state.jwt
        this.getSuppliers(1)
    },
    methods: {
        getSuppliers(page) {
            try {
                this.axios.get('suppliers?page='+page+'&search='+this.search.text, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.error = "Your session has expired. Please logout and login again."
                    } else {
                        this.suppliers = response.data[0].body
                        this.pages.page = response.data[0].page
                        this.pages.next = response.data[0].next
                        this.pages.prev = response.data[0].prev
                    }
                })
                .catch(e => {
                    this.response = e
                    this.error = "Internal Server Error"
                })
            } catch (error) {
                this.response = error
                this.error = "Internal Server Error"
            }
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