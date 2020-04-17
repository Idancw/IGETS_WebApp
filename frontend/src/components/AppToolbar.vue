<template>
  <div>
  <v-toolbar color="light-blue accent-1" fixed app>
    <v-toolbar-title>
      <router-link to="/" >
        <img class="logo" src="../assets/GEHC_logo.png" alt="GE Healthcare" v-on:click="reset">
      </router-link>
    </v-toolbar-title>
    <div class="hidden-sm-and-down">
      <v-select
        v-model="componentSection"
        :items="options"
        placeholder="Report"
        v-on:change="changeRoutToComponent($event)"
        persistent-hint
        >
      </v-select>
    </div>
    <div class="hidden-sm-and-down">
      <v-select
        v-model="runnerSection"
        :items="runnerOptions"
        placeholder="Runner"
        v-on:change="changeRoutToRunner($event)"
        >
      </v-select>
    </div>

    <div class="hidden-sm-and-down">
      <router-link to="/uploader">
        <v-btn flat>Uploader</v-btn>
      </router-link>
    </div>
<!--    <div class="hidden-sm-and-down">-->
<!--      <router-link to="/dataset_manager">-->
<!--        <v-btn flat>Dataset Manager</v-btn>-->
<!--      </router-link>-->
<!--    </div>-->
<!--    <div class="hidden-sm-and-down">-->
<!--      <router-link to="/evaluator">-->
<!--        <v-btn flat>Evaluator</v-btn>-->
<!--      </router-link>-->
<!--    </div>-->
  </v-toolbar>
  </div>

</template>

<script>
  import axios from 'axios'

  let BACKEND_URL = 'http://localhost:5000'

  export default {
    data () {
      return {
        componentSection: '',
        runnerSection: '',
        options: this.getComponentNamesFromBackend(),
        runnerOptions: ['Regression', 'Repeatability', 'Scalability', 'Performance']
      }
    },
    name: 'AppToolbar',
    methods: {
      getComponentNamesFromBackend () {
        const path = `${BACKEND_URL}/api/get_component_names`
        axios.get(path)
          .then(response => {
            this.options = response.data.component_names
          })
          .catch(error => {
            console.log(error)
          })
      },
      changeRoutToComponent (componentName) {
        this.$router.push({path: '/report/' + componentName})
        this.reset()
      },
      changeRoutToRunner (runnerName) {
        this.$router.push({path: '/runner/' + runnerName})
        this.reset()
      },
      reset () {
        // reset form to initial state
        this.componentSection = ''
        this.runnerSection = ''
      }
    }
  }
</script>

<style scoped>

  .logo {
    max-height: 60px;
    align-content: center;
    align-items: center;
  }

</style>
