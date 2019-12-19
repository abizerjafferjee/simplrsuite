<template>
    <div id="category-view">

        <div class="notification" v-if="error">
            <button @click="closeNotification" class="delete"></button>
            {{ error }}
        </div>

        <section class="welcome card card-content has-background-light">
            <div class="columns">
                <div class="column is-four-fifths">
                    <div class="field is-grouped">
                        <p class="control is-expanded">
                            <input v-model="category.name" class="input" type="text" placeholder="Type category name">
                        </p>
                        <a @click="addCategory()" class="button is-info">Add Category</a>
                    </div>
                </div>
                <div class="column"></div>
            </div>
        </section>

        <div class="section">
            <div class="notification" v-if="categories">You have {{ categories.length }} categories</div>
            <div class="notification" v-else>You have no categories. Add a new category.</div>
        </div>            

        <div class="section" v-if="categories">

            <div class="card-table">
                <table class="card-body table is-stripped">
                    <thead>
                        <tr>
                            <th>Category Id</th>
                            <th>Category</th>
                            <th>Number of Products</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="category in categories" :key="category.id">
                            <td>{{ category.id }}</td>
                            <td v-if="editing === category.id"><input type="text" v-model="category.name"></td>
                            <td v-else>{{ category.name }}</td>
                            <td v-if="category.products">{{ category.products.length }}</td>

                            <td v-if="editing == category.id">
                                <button class="button is-small is-success" @click="editCategory(category)"><font-awesome-icon class="font-margin" icon="save" size="lg" /></button>&nbsp;
                                <button class="button is-small muted-button" @click="cancelEdit(category)"><font-awesome-icon class="font-margin" icon="times" size="lg" /></button>
                            </td>
                            <td v-else>
                                <button class="button is-small is-info" @click="editMode(category)"><font-awesome-icon class="font-margin" icon="pen" size="lg" /></button>&nbsp;
                                <button class="button is-small is-danger" @click="deleteCategory(category.id)"><font-awesome-icon class="font-margin" icon="trash" size="lg" /></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <footer class="card-footer level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getCategories(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getCategories(pages.page+1)">Next page</a>
                </footer>
            </div>

        </div>

    </div>
</template>

<script>

export default {
    name: 'category-view',
    components: {
    },
    data() {
        return {
            jwt: '',
            editing: null,
            response: null,
            error: null,
            category: {
                name: '',
            },
            categories: [],
            pages: {
                page: null,
                next: null,
                prev: null
            },
        }
    },
    created() {
        this.jwt = this.$store.state.jwt
        this.getCategories(1)
    },
    methods: {
        getCategories(page) {
            this.axios.get('categories?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.categories = response.data.categories
                this.pages.page = response.data.page
                this.pages.next = response.data.next
                this.pages.prev = response.data.prev
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        deleteCategory(id) {
            this.axios.delete('categories?id='+id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.getCategories(this.pages.page)
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        addCategory() {
            if (this.invalidCategory()) {
                this.error = "Cannot add empty category"
            } else {
                this.axios.post('categories', {'body': this.category}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    this.getCategories(this.pages.page)
                })
                .catch(error => {
                    if (error.response.status === 401) {
                        this.error = "Your session has expired. Please login again."
                    } else {
                        this.error = "Internal Server Error"
                    }
                })
            }
        },
        editCategory(updatedCategory) {
            this.axios.put('categories?id='+updatedCategory.id, {'body': updatedCategory}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.getCategories(this.pages.page)
                this.editing = null
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        editMode(category) {
            this.cachedCategory = Object.assign({}, category);
            this.editing = category.id
        },
        cancelEdit(category) {
            Object.assign(category, this.cachedCategory)
            this.editing = null
        },
        closeNotification() {
            this.error = null
        },
        invalidCategory() {
            if (this.category.name === '') {
                return true
            }
            return false
        },
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
.font-margin {
    margin: 0px 5px 0px 5px;
}
</style>