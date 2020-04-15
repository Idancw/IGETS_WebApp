<template>
  <v-container id="ComponentReportViewer" fluid grid-list-xl style="max-width: 78%">

    <div style="margin-top: 10%">
      {{ route_path }}

    </div>
    <template>
        <v-data-table
        :headers="headers"
        :items="desserts"
        :loading="loading"
        fixed
        style="overflow-y: auto; overflow-x: auto"
        no-data-text="No data to display"
        :sort-by="['calories', 'fat']"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      >
          <template slot="items" slot-scope="props">
            <tr>
              <td>{{ props.item.name }}</td>
              <td class="text-xs-right">{{ props.item.calories }}</td>
              <td class="text-xs-right">{{ props.item.fat }}</td>
              <td class="text-xs-right">{{ props.item.carbs }}</td>
              <td class="text-xs-right">{{ props.item.protein }}</td>
              <td class="text-xs-right">{{ props.item.iron }}</td>
            </tr>
          </template>
        </v-data-table>
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
        reportData: [],
        loading: false,
        saving: false,
        showDataset: false,
        data: {},
        options: {},
        savePath: null,
        saveEnable: true,
        hideRow: false,
        hideHeaderRow: false,
        rows: [],
        drawer: false,
        headers: [
          {
            text: 'Dessert (100g serving)',
            align: 'start',
            sortable: false,
            value: 'name'
          },
          { text: 'Calories', value: 'calories' },
          { text: 'Fat (g)', value: 'fat' },
          { text: 'Carbs (g)', value: 'carbs' },
          { text: 'Protein (g)', value: 'protein' },
          { text: 'Iron (%)', value: 'iron' }
        ],
        desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 200,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            iron: '1%'
          },
          {
            name: 'Ice cream sandwich',
            calories: 200,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            iron: '1%'
          },
          {
            name: 'Eclair',
            calories: 300,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            iron: '7%'
          },
          {
            name: 'Cupcake',
            calories: 300,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            iron: '8%'
          },
          {
            name: 'Gingerbread',
            calories: 400,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            iron: '16%'
          },
          {
            name: 'Jelly bean',
            calories: 400,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            iron: '0%'
          },
          {
            name: 'Lollipop',
            calories: 400,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            iron: '2%'
          },
          {
            name: 'Honeycomb',
            calories: 400,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            iron: '45%'
          },
          {
            name: 'Donut',
            calories: 500,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            iron: '22%'
          },
          {
            name: 'KitKat',
            calories: 500,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            iron: '6%'
          }
        ]
      }
    },
    methods: {
      getJson(option) {
        // this.data = this.getJsonFromBackend(option)
      },
      getReportDataFromBackend() {
        let componentName = this.route_path.split('/')[this.route_path.split('/').length - 1]

        const path = `${BACKEND_URL}/api/get_component_report/` + componentName
        axios.get(path)
          .then(response => {
            console.log('Here')
            // this.data = response.data.data
            // this.savePath = option
            // for (let i = 0; i < this.data.images.length; ++i) {
            //   this.rows = this.rows.concat([false])
            // }
            // let idx = 0
            // for (let item in this.data) {
            //   let len = this.data[item].length
            //   for (let j = 0; j < len; ++j) {
            //     this.checkInRows(this.data[item][j]['tags'], idx)
            //     idx++
            //   }
            // }
          })
          .catch(error => {
            console.log(error)
          })
        // this.showDataset = true
        // this.saveEnable = false
      },
      postJsonToBackend() {
        if (this.savePath) {
          const path = `${BACKEND_URL}/api/savejson/` + this.savePath
          axios.post(path, this.data)
            .then(response => {

            })
            .catch(error => {
              console.log(error)
            })
          this.showDataset = false
          this.savePath = null
          this.saveEnable = true
          this.hideRow = false
          this.hideHeaderRow = false
          this.rows = []
          this.drawer = false
        }
      },
      getDatasetOptions() {
        console.log('dasdasdasdas')
        console.log(this.$route)
        this.options = this.getDatasetOptionsFromBackend()
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
      disableChecks(tags, currTag, index) {
        for (let i = 0; i < tags.length; i++) {
          if (tags[i].label !== currTag) {
            tags[i].checked = false
          }
        }
        this.checkInRows(tags, index)
      },
      checkInRows(tags, index) {
        let checkedFlag = false
        for (let i = 0; i < tags.length; i++) {
          if (tags[i].checked) {
            checkedFlag = true
          }
        }
        this.rows[index] = checkedFlag
        this.hideHeaderRow = this.hideHeader()
      },
      hideHeader() {
        for (let i = 0; i < this.rows.length; ++i) {
          if (!this.rows[i]) {
            return false
          }
        }
        return true
      }
    },
    created() {
      this.getReportDataFromBackend()
    },
    watch: {
      $route (to, from) {
        this.route_path = this.$route.path
        this.getReportDataFromBackend()
      }
    }
  }
  </script>

<style scoped>
  table.v-table tbody td,
    table.v-table tbody th {
    height: 19px;
  }

  .page-content {
    display: flex;
    flex-direction: column;
    margin: auto;
  }

  .first_row {
    -webkit-box-pack: start;
  }

  .content-row-header {
    display: flex;
    flex: 1;
    /*justify-content: center;*/
    align-content: center;
    align-items: center;
    font-size: 42px;
    font-family: Ubuntu;
    font-weight: bold;
  }

  .content-row {
    display: flex;
    flex: 5;

  }

  .content-col {
    display: -webkit-box;
    flex: 1;
    align-content: center;
    align-items: center;
    overflow-x: auto;
    border: 1px solid #cccccc;
    height: 100%;
    border-radius: 20px;

  }

  .tags{
    /*display: inline;*/
  }

  .item {
    float: left;
    width: 50%;
    padding: 5px;
  }

  .image {
    display: block;
    border: 1px solid #ddd;
    border-radius: 10%;
    margin: 2%;
    width: 100%;
  }

  .center {
    justify-content: center;
    align-content: center;
    align-items: center;
  }

  select#soflow, select#soflow-color {
    -webkit-box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
    -webkit-padding-end: 20px;
    -webkit-padding-start: 2px;
    -webkit-user-select: none;
    background-image: url(http://i62.tinypic.com/15xvbd5.png), -webkit-linear-gradient(#F1F1F1, #F4F4F4);
    background-position: 97% center;
    color: #555;
    font-size: inherit;
    margin:8px;
    overflow: hidden;
    padding: 8px 10px;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 90%;
  }

  .logo {
    max-height: 60px;
    align-content: center;
    align-items: center;
  }

  .navBtn {
    width: 100%;
  }
</style>
