<template>
  <div id="app" class="container is-fullhd">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <!-- <a class="navbar-item" href="https://bulma.io"> -->
          <img src="./assets/logo_2.jpg" width="150" height="150">
        <!-- </a> -->
      </div>
    </nav>

    <div class="columns">
      <div class="column is-one-fifth">
        <aside class="menu">
          <ul class="menu-list">
            <li><router-link to="/dashboard">Dashboard</router-link></li>
            <li><router-link to="/add-contact">Mailing List</router-link></li>
          </ul>
          <p class="menu-label">
            Procurement
          </p>
          <ul class="menu-list">
            <li><router-link to="/products">Products</router-link></li>
            <!-- <li><router-link to="/add-product">Add Product</router-link></li> -->
            <li><router-link to="/suppliers">Suppliers</router-link></li>
            <!-- <li><router-link to="/add-supplier">Add Supplier</router-link></li> -->
            <li><router-link to="/inventory">Inventory</router-link></li>
            <!-- <li><router-link to="/add-inventory">Add Inventory</router-link></li> -->
            <li><a>Payments</a></li>
            <!-- <li><router-link to="/add-inventory">Stocking Note</router-link></li> -->
          </ul>
          <!-- <p class="menu-label">
            Sales
          </p>
          <ul class="menu-list">
            <li><a>Customers</a></li>
            <li><a>Orders</a></li>
            <li><a>Credit Note</a></li>
          </ul>
          <p class="menu-label">
            Resources
          </p>
          <ul class="menu-list">
            <li><a>Employees</a></li>
          </ul> -->
        </aside>
      </div>

      <div class="column">
        <router-view></router-view>
        <!-- <h1>Add Products</h1> -->
        <!-- <product-form @add:product="addProduct" /> -->
        <!-- <product-table v-bind:products="products" @delete:product="deleteProduct" @edit:product="editProduct" /> -->
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'app',
}
</script>

<style>
@import "~bulma/css/bulma.css";
</style>
