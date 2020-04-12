<template>
  <div>

  <v-toolbar color="orange darken-2" dark fixed app>
    <v-toolbar-title>
      <router-link to="/">
        <img class="logo" src="../assets/logo.jpg">
      </router-link>
    </v-toolbar-title>
    <div class="hidden-sm-and-down">
      <router-link to="/uploader">
        <v-btn flat>Dataset Uploader</v-btn>
      </router-link>
    </div>
    <div class="hidden-sm-and-down">
      <router-link to="/dataset_manager">
        <v-btn flat>Dataset Manager</v-btn>
      </router-link>
    </div>
    <div class="hidden-sm-and-down">
      <router-link to="/evaluator">
        <v-btn flat>Evaluator</v-btn>
      </router-link>
    </div>


  </v-toolbar>
  </div>
</template>

<script>
  export default {
    name: 'AppToolbar'
  }
</script>

<style scoped>

  .logo {
    max-height: 60px;
    align-content: center;
    align-items: center;
  }

</style>
