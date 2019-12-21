<template>
    <div id="category-view">

        <div class="level">
            <div class="title is-6 has-text-danger" v-if="error">{{ error }}</div>
            <div class="title is-6 has-text-success" v-else-if="success">{{ success }}</div>
            <div v-else></div>
        </div>

        <article class="card has-text-centered">
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                <div class="column is-four-fifths">
                    <div class="field is-grouped">
                        <p class="control is-expanded">
                            <input v-model="category" @focus="clearStatus" class="input" type="text" placeholder="Type category name">
                        </p>
                        <a @click="addCategory()" class="button is-primary">Add Category</a>
                    </div>
                </div>
                <div class="column"></div>
                </div>
            </div>
            <div class="card has-background-info has-text-white is-paddingless">
                <div class="level">
                    <div class="column">Category Id</div>
                    <div class="column is-two-fifths">Category</div>
                    <div class="column">Number of Products</div>
                    <div class="column">Actions</div>
                </div>
            </div>
            <!-- <div class="card has-background-info is-paddingless" v-if="categories && categories.length>0">
                <div class="column"><div class="title is-5 has-text-white">You have {{ categories.length }} categories.</div></div>
            </div> -->
            <div class="has-background-light" style="min-height:500px">
                <div class="notification" v-if="categories && categories.length===0">You have no categories. Add a new category.</div>
                <div class="card is-paddingless" v-for="category in categories" :key="category.id" v-else-if="categories && categories.length > 0">
                    <div class="level">
                        <div class="column"><div class="title is-6">{{ category.id }}</div></div>
                        <div class="column is-two-fifths">
                            <div class="title is-6" v-if="editing === category.id"><input type="text" v-model="category.name"></div>
                            <div class="title is-6" v-else>{{ category.name }}</div>
                        </div>
                        <div class="column"><div class="title is-6" v-if="category.products">{{ category.products.length }}</div></div>

                        <div class="column" v-if="editing == category.id">
                            <button class="button is-small is-success" @click="editCategory(category)"><font-awesome-icon class="font-margin" icon="save" size="lg" /></button>&nbsp;
                            <button class="button is-small muted-button" @click="cancelEdit(category)"><font-awesome-icon class="font-margin" icon="times" size="lg" /></button>
                        </div>
                        <div class="column" v-else>
                            <button class="button is-small is-info" @click="editMode(category)"><font-awesome-icon class="font-margin" icon="pen" size="lg" /></button>&nbsp;
                            <button class="button is-small is-danger" @click="deleteCategory(category.id)"><font-awesome-icon class="font-margin" icon="trash" size="lg" /></button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card is-paddingless">
                <div class="level">
                    <a class="pagination-previous level-left" title="This is the first page" :disabled="pages.prev==false" @click="getCategories(pages.page-1)">Previous</a>
                    <a class="pagination-next level-right" :disabled="pages.next==false" @click="getCategories(pages.page+1)">Next page</a>
                </div>
            </div>
        </article>

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
            error: null,
            success: null,
            editing: null,
            response: null,
            category: null,
            categories: null,
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
                this.success = "Category deleted."
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
            this.axios.post('categories', {'body': this.category}, { headers: { Authorization: `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Category added."
                this.getCategories(this.pages.page)
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status === 400) {
                    this.error = error.response.data['message']
                } else {
                    this.error = "Internal Server Error"
                }
            })
        },
        editCategory(updatedCategory) {
            this.axios.put('categories?id='+updatedCategory.id, {'body': updatedCategory}, { headers: {'Content-Type': 'application/json', 'Authorization': `Bearer: ${this.jwt}`}})
            .then(response => {
                this.response = response
                this.success = "Category updated."
                this.editing = null
                this.getCategories(this.pages.page)
            })
            .catch(error => {
                if (error.response.status === 401) {
                    this.error = "Your session has expired. Please login again."
                } else if (error.response.status === 400) {
                    this.error = error.response.data['message']
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
        clearStatus() {
            this.error = null
            this.success = null
            this.category = ''
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