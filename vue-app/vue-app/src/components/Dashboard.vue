<template>
    <div id="dashboard">
        <div class="tile is-ancestor">
            <div class="tile is-vertical is-8">
                <div class="tile">
                <div class="tile is-parent is-vertical">
                    <article class="tile is-child notification is-primary">
                    <p class="title">Payments</p>
                    <p class="subtitle">Total to be Paid</p>
                    </article>
                    <article class="tile is-child notification is-warning">
                    <p class="title">Payment History</p>
                    <p class="subtitle">Last 10 Payments</p>
                    </article>
                </div>
                <div class="tile is-parent">
                    <article class="tile is-child notification is-info">
                    <p class="title">Customers</p>
                    <p class="subtitle">With an image</p>
                    <figure class="image is-4by3">
                        <img src="https://bulma.io/images/placeholders/640x480.png">
                    </figure>
                    </article>
                </div>
                </div>
                <div class="tile is-parent">
                <article class="tile is-child notification is-danger">
                    <p class="title">Products</p>
                    <p class="subtitle">Fastest Moving Inventory</p>
                    <div class="content">
                    <!-- Content -->
                    </div>
                </article>
                </div>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-success">
                <div class="content">
                    <p class="title">Sales</p>
                    <p class="subtitle">Daily Sales Record</p>
                    <div class="content">
                    <!-- Content -->
                    </div>
                </div>
                </article>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'dashboard',
    data() {
        return {
            response: null,
        }
    },
    mounted() {
    },
    methods: {
    }
}
</script>


<style scoped>
button {
    margin: 0 0.5 rem 0;
}
</style>