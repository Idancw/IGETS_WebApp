<template>
    <v-app id="inspire">
      <!--<app-navigator></app-navigator>-->
      <app-toolbar></app-toolbar>
      <div style="padding-top: 0px">
        <router-view/>
      </div>
      <app-footer></app-footer>
    </v-app>
</template>

<script>
  import AppToolbar from './components/AppToolbar'
  import AppFooter from './components/AppFooter'

  export default {
    components: {AppFooter, AppToolbar},
    data: () => ({
      name: 'App'
    })
  }
</script>










