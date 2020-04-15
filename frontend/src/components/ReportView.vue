<template>
  <v-container id="ComponentReportViewer" fluid grid-list-xl style="max-width: 78%; padding-top: 5%">
    <div>
      <v-btn class="ma-2" tile color="indigo" dark @click="$router.back()">Back</v-btn>
      <span id="reportHtml"></span>
    </div>
    <br>
    <br>
  </v-container>
</template>

<script>
  /* eslint-disable space-before-function-paren */
  import axios from 'axios'

  // CONST backend Url
  let BACKEND_URL = 'http://localhost:5000'

  export default {
    name: 'ComponentReportViewer',
    data() {
      return {
        route_path: this.$route.path,
        reportBackendPath: this.$route.query.reportFile,
        reportContent: null
      }
    },
    methods: {
      report() {
        let refactorPath = this.reportBackendPath.replaceAll('/', '!')
        const backendPath = `${BACKEND_URL}/api/get_report_html/` + refactorPath
        this.enableReportTable = false
        axios.get(backendPath)
        .then(response => {
          this.reportContent = response.data.result
          console.log(this.reportContent)
          document.getElementById('reportHtml').innerHTML = this.reportContent
        })
        .catch(error => {
            console.log(error)
          })
      }
    },
    created() {
      this.report()
    },
    watch: {
      // $route (to, from) {
      //   this.route_path = this.$route.path
      // }
    }
  }
  </script>

<style scoped>
  table.v-table tbody td,
    table.v-table tbody th {
    text-align: center!important;
    height: 19px;
  }
</style>
