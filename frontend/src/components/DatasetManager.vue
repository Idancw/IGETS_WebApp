<template>
  <v-container id="DatasetManager" fluid grid-list-xl style="max-width: 78%">
    <!--Adds to navbar buttons shortcuts-->
    <v-navigation-drawer
      v-model="drawer"
      fixed
      app
    >
      <v-card>
        <v-toolbar>
          <v-toolbar-title>Options</v-toolbar-title>
        </v-toolbar>
        <v-btn :loading="saving" :disabled="saveEnable" @click.native="saver = 'saving'" @click="postJsonToBackend"
          flat class="navBtn">
          <v-icon left>save</v-icon>
          Save
        </v-btn>
        <v-btn @click="hideRow = !hideRow" :disabled="saveEnable" flat class="navBtn">
          <v-icon v-if="hideRow" left>visibility_off</v-icon>
          <v-icon v-else left>visibility</v-icon>
          {{ hideRow ? 'Show all' : 'Hide checked rows' }}

        </v-btn>
      </v-card>
    </v-navigation-drawer>
    <!--END-->

    <br>
    <v-toolbar color="orange darken-2" dark fixed app>
      <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
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
    <v-container >
      <div class="row col-lg-6 input-group center">
        <v-layout row>
          <v-flex xs8>
            <select id="soflow" @click="getDatasetOptions">
              <option value="">Please select dataset</option>
              <option v-for="option in options" @click="getJson(option)">{{ option }}</option>
            </select>
          </v-flex>
          <v-flex xs4>
            <v-btn
              :loading="saving"
              :disabled="saveEnable"
              style="padding: 1px 35px;"
              color="blue-grey lighten-4"
              @click.native="saver = 'saving'"
              @click="postJsonToBackend"
            >
              Save
            </v-btn>
            <v-btn @click="hideRow = !hideRow" :disabled="saveEnable" class="right">
              {{ hideRow ? 'Show all' : 'Hide checked rows' }}
            </v-btn>
          </v-flex>
        </v-layout>
      </div>
    </v-container>
    <v-layout wrap v-if="showDataset === true" style="padding: 5% 5% 5% 6%;">
      <div class="page-content">
        <div class="content-row-header" v-show="!(hideHeaderRow && hideRow)">
          <div class="content-col center first_row">Instance</div>
          <div class="content-col center first_row">Tags</div>
        </div>
        <div class="content-row" v-for="(item, index) in data.images" v-show="!(hideRow && rows[index])">
          <div class="content-col">
            <div class="item" v-for="image in item.uri">
              <img class='image'
                   :src="image">
            </div>
          </div>
          <div class="content-col">
            <div >
              <v-btn v-for="(tag,i) in item.tags" class="tags" :key="i"
                     v-on:click="tag.checked = !tag.checked"
                     v-on:click.prevent="disableChecks(item.tags, tag.label, index)"
                     v-bind:class="{'green': tag.checked }"
              >
                {{tag.label}}
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-layout>

  </v-container>
</template>

<script>
  /* eslint-disable space-before-function-paren */
  import axios from 'axios'
  // CONST backend Url
  let BACKEND_URL = 'http://localhost:5000'

  export default {
    data() {
      return {
        saver: null,
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
        drawer: false
      }
    },
    methods: {
      getJson(option) {
        this.data = this.getJsonFromBackend(option)
      },
      getJsonFromBackend(option) {
        if (!option || !(typeof option === 'string')) {
          return
        }
        const path = `${BACKEND_URL}/api/loadjson/` + option
        axios.get(path)
          .then(response => {
            this.data = response.data.data
            this.savePath = option
            for (let i = 0; i < this.data.images.length; ++i) {
              this.rows = this.rows.concat([false])
            }
            let idx = 0
            for (let item in this.data) {
              let len = this.data[item].length
              for (let j = 0; j < len; ++j) {
                this.checkInRows(this.data[item][j]['tags'], idx)
                idx++
              }
            }
          })
          .catch(error => {
            console.log(error)
          })
        this.showDataset = true
        this.saveEnable = false
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
      this.getJson()
    },
    watch: {
      saver() {
        const l = this.saver
        this[l] = !this[l]
        setTimeout(() => (this[l] = false), 1500)
        this.saver = null
      }
    }
  }
  </script>

<style scoped>
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
