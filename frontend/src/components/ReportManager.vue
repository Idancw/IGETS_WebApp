<template>
  <v-container id="ComponentReportViewer" fluid grid-list-xl style="max-width: 78%; padding-top: 5%">
    <template>
        <v-data-table
        :headers="tableHeaders"
        :items="tableRows"
        fixed
        style="overflow-y: auto; overflow-x: auto"
        no-data-text="No data to display"
        :sort-desc="[false, true]"
        multi-sort="true"
      >
          <template slot="items" slot-scope="props">
            <tr>
              <td class="text-xs-center">{{ props.item.Date }}</td>
              <td class="text-xs-left">{{ props.item.Time }}</td>
              <td class="text-xs-left">{{ props.item.Golden }}</td>
              <td class="text-xs-left">{{ props.item.Candidate }}</td>
              <td class="text-xs-left">{{ props.item.Completed }}</td>
              <td class="text-xs-left">{{ props.item.State }}</td>
              <td class="text-xs-left">
                <router-link v-if="props.item.Report_link"
                             :to="{path: route_path + '/report_view', query: { reportFile: props.item.Report_link }}"
                             >link</router-link>
                <span v-else>---</span>
              </td>
            </tr>
          </template>
        </v-data-table>
        <v-btn class="ma-2" tile color="indigo" dark @click="refreshTable()">Refresh</v-btn>
    </template>
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
        tableData: [],
        tableHeaders: [
          {text: 'Date (YYYY-MM-DD)', align: 'start', value: 'Date'},
          {text: 'Time (hh:mm:ss)', value: 'Time'},
          {text: 'Golden version', value: 'Golden'},
          {text: 'Candidate version', value: 'Candidate'},
          {text: 'Completed', value: 'Completed'},
          {text: 'State', value: 'State'},
          {text: 'Report_link', value: 'Report_link'}
        ],
        tableRows: []
      }
    },
    methods: {
      getReportDataFromBackend() {
        let componentName = this.route_path.split('/')[this.route_path.split('/').length - 1]
        const path = `${BACKEND_URL}/api/get_component_report/` + componentName
        axios.get(path)
          .then(response => {
            this.reportTable = response.data.result
            for (let key in this.reportTable) {
              if (this.reportTable.hasOwnProperty(key)) {
                let rowInfo = {Date: this.reportTable[key].Date,
                  Time: this.reportTable[key].Time,
                  Golden: this.reportTable[key].Golden,
                  Candidate: this.reportTable[key].Candidate,
                  Completed: this.reportTable[key].Completed,
                  State: this.reportTable[key].State,
                  Report_link: this.reportTable[key].Report_link}
                this.tableRows.push(rowInfo)
              }
            }
          })
          .catch(error => {
            console.log(error)
          })
      },
      refreshTable() {
        this.reset()
        this.getReportDataFromBackend()
      },
      getDatasetOptionsFromBackend() {
        const path = `${BACKEND_URL}/api/getoptions`
        axios.get(path)
          .then(response => {
            this.options = response.data.options
          })
          .catch(error => {
            console.log(error)
          })
      },
      reset() {
        this.tableRows = []
      }
    },
    created() {
      this.reset()
      this.getReportDataFromBackend()
    },
    watch: {
      $route (to, from) {
        this.route_path = this.$route.path
        this.getReportDataFromBackend()
        this.reset()
      }
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
