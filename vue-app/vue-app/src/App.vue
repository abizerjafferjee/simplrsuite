<template>
  <div id="app" class="container is-fullhd">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <!-- <a class="navbar-item" href="https://bulma.io"> -->
          <img src="./assets/logo_2.jpg" width="150" height="150">
          <!-- Simplr Suite</a> -->
        <!-- </a> -->
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link to="/signup" class="button is-primary">
              <strong>Sign Up</strong>
            </router-link>
            <router-link to="/signin" class="button is-light">
              Log in
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="columns">
      <div class="column is-one-fifth">
        <aside class="menu is-size-5">
          <ul class="menu-list">
            <li><router-link to="/dashboard"><font-awesome-icon class="icon has-text-info font-margin" icon="chart-line" size="lg" />Dashboard</router-link></li>
            <li><router-link to="/add-contact"><font-awesome-icon class="font-margin" icon="at" size="lg" />Mailing List</router-link></li>
          </ul>
          <p class="menu-label">
            Procurement
          </p>
          <ul class="menu-list">
            <li><router-link to="/products"><font-awesome-icon class="icon has-text-info font-margin" icon="store" size="lg" />Products</router-link></li>
            <li><router-link to="/suppliers"><font-awesome-icon class="icon has-text-danger font-margin" icon="truck" size="lg" />Suppliers</router-link></li>
            <li><router-link to="/inventory"><font-awesome-icon class="font-margin" icon="warehouse" size="lg" />Inventory</router-link></li>
            <li><router-link to="/payments"><font-awesome-icon class="icon has-text-success font-margin" icon="money-check-alt" size="lg" />Payments</router-link></li>
          </ul>
        </aside>
      </div>

      <div class="column is-size-5">
        <router-view></router-view>
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
#app {
  min-width: 75%;
}
.font-margin {
    margin: 0px 5px 0px 0px;
}
</style>
