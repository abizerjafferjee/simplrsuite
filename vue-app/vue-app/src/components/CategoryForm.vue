<template>
   <div id="category-form">
        <div class="tile is-parent">
            <article class="tile is-child">
                <p class="title">Add Category</p>

                <div class="notification" v-if="errorNotification">
                    <button @click="closeNotification" class="delete"></button>
                    {{ errorNotification }}
                </div>         
                <br>

                <div class="content">
                    <form @submit.prevent="handleSubmit">
                        <label>Category Name</label>
                        <input ref="name" @focus="clearStatus" @keypress="clearStatus" v-model="category.name" type="text" />

                        <p v-if="error && submitting" class="error-message">!Please fill out all required fields</p>
                        <p v-if="success" class="success-message">Category successfully added</p>
                        
                        <button>Add Category</button>
                    </form>
                </div>
            </article>
        </div>

   </div> 
</template>

<script>
export default {
    name: 'category-form',
    data() {
        return {
            submitting: false,
            error: false,
            success: false,
            errorNotification: null,
            category: {
                name: '',
            },
            jwt: ''
        }
    },
   created: function() {
       this.jwt = this.$store.state.jwt
   },
    methods: {
       handleSubmit() {
           this.submitting = true
           this.clearStatus()
           this.$emit('add:category', this.category)
           this.error = false
           this.success = true
           this.submitting = false
           this.$refs.name.focus()
       },
       clearStatus() {
           this.error = false
           this.success = false
       },
        closeNotification() {
            this.errorNotification = null
        }
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