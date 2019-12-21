<template>
   <div id="category-form">
        <div class="section">
            <p class="title is-4">Add Category</p>
            <form @submit.prevent="handleSubmit">
                <label>Category Name</label>
                <input ref="name" v-model="category" type="text" />                
                <button>Add Category</button>
            </form>
        </div>

   </div> 
</template>

<script>
export default {
    name: 'category-form',
    data() {
        return {
            jwt: '',
            category: null,
        }
    },
   created: function() {
       this.jwt = this.$store.state.jwt
   },
    methods: {
       handleSubmit() {
           this.$emit('add:category', this.category)
       },
    }
}
</script>

<style scoped>
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