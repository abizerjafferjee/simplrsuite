<template>
    <div id="category-view">
        <div class="tile is-parent">
            <article class="tile is-child">

                <section class="hero is-light welcome is-small">
                    <div class="hero-body">
                        <div class="container level">
                            <h1 class="title level-left">
                                Manage Categories
                            </h1>
                        </div>
                    </div>
                </section>
                <br>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>

                <div class="field is-grouped">
                    <p class="control is-expanded">
                        <input v-model="category.name" class="input" type="text" placeholder="Type category name">
                    </p>
                    <p class="control">
                        <a @click="addCategory()" class="button is-info">Add Category</a>
                    </p>
                </div>

                <div v-if="!categories" class="notification">
                    You have no categories.
                </div>

                <div class="notification" v-else>
                    You have {{ categories.length }} categories
                </div>            

                <div class="content" v-if="categories">

                    <div class="card-table">
                        <table class="card-body table is-stripped">
                            <thead>
                                <tr>
                                    <th>Category Id</th>
                                    <th>Category</th>
                                    <th>Number of Products</th>
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
            </article>
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
            categories: [],
            category: {
                name: '',
            },
            pages: {
                page: null,
                next: null,
                prev: null
            },
            editing: null,
            response: null,
            error: null,
            errorNotification: null,
            jwt: ''
        }
    },
    created() {
        this.jwt = this.$store.state.jwt
        this.getCategories(1)
    },
    methods: {
        getCategories(page) {
            try {
                this.axios.get('categories?page='+page, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.error = "Your session has expired. Please logout and login again."
                    } else {
                        this.categories = response.data[0].categories
                        console.log(this.categories)
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
        deleteCategory(id) {
            try {
                this.axios.delete('categories?id='+id, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.getCategories(this.pages.page)
                    }
                })
                .catch(error => {
                    this.response = error
                    this.errorNotification = "Internal Server Error: delete category."
                })
            } catch (error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
        },
        addCategory() {
            try {
                if (this.invalidCategory()) {
                    this.errorNotification = "Cannot add empty category"
                } else {
                    this.axios.post('categories', {'body': this.category}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
                    .then(response => {
                        if (response.data[1] === 401) {
                            this.response = response
                            this.errorNotification = "Your session has expired. Please logout and login again."
                        } else {
                            this.getCategories(this.pages.page)
                        }
                    })
                    .catch(e => {
                        this.response = e
                        this.errorNotification = "Internal Server Error: add category."
                    })
                }
            } catch (error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
        },
        editCategory(updatedCategory) {
            try {
                this.axios.put('categories?id='+updatedCategory.id, {'body': updatedCategory}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
                .then(response => {
                    if (response.data[1] === 401) {
                        this.response = response
                        this.errorNotification = "Your session has expired. Please logout and login again."
                    } else {
                        this.response = response
                        this.getCategories(this.pages.page)
                        this.editing = null
                    }
                })
                .catch(error => {
                    this.response = error
                    this.errorNotification = "Internal Server Error: edit category"
                })
            } catch(error) {
                this.response = error
                this.errorNotification = "Connection Error."
            }
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
            this.errorNotification = null
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