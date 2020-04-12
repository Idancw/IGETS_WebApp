<!--suppress ALL -->
<template>
  <div id="evaluator" style="margin-top: 5%">
    <v-layout justify-center>
      <v-flex xs12 sm10 md8 lg6>
        <v-card ref="form">
          <div v-if="isInitial || isEvaluate">
            <v-select
              name="GT_dataset"
              :rules="[() => !!GT_dataset || 'This field is required']"
              :items="options"
              v-model="GT_dataset"
              autocomplete
              label="GT dataset"
              placeholder="Select..."
              required
              @mouseover="getDatasetOptions"
              @click.capture="isActive">
            </v-select>
            <h4>Upload algorithm dataset</h4>
            <br>
            <input type="file" multiple
                   :name="uploadFieldName"
                   @change="filesChange($event.target.name, $event.target.files)">
            <v-divider class="mt-5"></v-divider>

            <v-card-actions class="text-xs-center">
              <v-btn
                color="primary"
                flat
                @click="evaluate"
                :disabled="!evaluateEnable"
              >
                Evaluate
              </v-btn>
            </v-card-actions>
          </div>
          <div v-else>
            <div>
              <p>
                <v-btn
                  color="orange lighten-5"
                  block
                  @click="reset"
                >
                  Start over
                </v-btn>
              </p>
              <div v-if="isSuccess">
                <v-card>
                  <v-toolbar color="green" dark>
                    <v-toolbar-title>Evaluation result:</v-toolbar-title>
                    <v-spacer></v-spacer>
                  </v-toolbar>
                  <div v-if="warningsLen">
                    <div>
                      <v-badge>
                        <span v-if="!alert" slot="badge">{{ warningsLen }}</span>
                        <v-btn color="warning" @click="alert = !alert">
                          {{ alert ? 'Hide Warnings' : 'Show Warnings' }}
                          <v-icon v-if="alert" right>visibility_off</v-icon>
                          <v-icon v-else right>visibility</v-icon>
                        </v-btn>
                      </v-badge>
                    </div>
                    <div v-for="warn in warnings">
                      <v-alert :value="true" type="warning" v-show="alert">
                        {{ warn }}
                      </v-alert>
                    </div>
                  </div>
                  <v-subheader>
                    Confusion Matrix
                  </v-subheader>
                  <img id="CM_image" :src=CM>
                  <div>
                    <v-btn
                      color="orange lighten-3"
                      @click.native="showCM = !showCM"
                      @click="showCMTable()">
                      {{ showCM ? 'Show CM table' : 'Hide CM table' }}
                    </v-btn>
                    <v-btn
                      color="orange lighten-3"
                      @click.native="showDetailed = !showDetailed"
                      @click="showDetailedTable()">
                      {{ showDetailed ? 'Show Detailed table' : 'Hide Detailed table' }}
                    </v-btn>
                    <p class="accuracy">
                      Accuracy: {{ accuracy }}
                    </p>
                  </div>
                  <div>
                    <p id="CMtable"></p>
                    <p id="Detailedtable"></p>
                    <br>
                    <br>
                    <br>
                  </div>
                </v-card>
              </div>
              <div v-if="isFailed">
                <v-card>
                  <v-toolbar color="red" dark>
                    <v-toolbar-title>Upload Failed</v-toolbar-title>
                    <v-spacer></v-spacer>
                  </v-toolbar>
                  <v-subheader>
                    Error massage: {{ uploadError }}
                  </v-subheader>
                </v-card>
              </div>
              <div></div>
            </div>
          </div>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
  import axios from 'axios'
  import {upload} from '../scripts/file-upload.service'

  const STATUS_INITIAL = 0
  const STATUS_EVALUATING = 1
  const STATUS_SUCCESS = 2
  const STATUS_FAILED = 3

  export default {
    name: 'Evaluator',
    data () {
      return {
        uploadFieldName: 'Algo_dataset',
        options: [],
        GT_dataset: '',
        Algorithm_dataset: '',
        uploadError: '',
        formHasErrors: false,
        evaluateEnable: false,
        currentStatus: STATUS_INITIAL,
        formData: null,
        CM: null,
        CMTable: null,
        detailedTable: null,
        showCM: true,
        showDetailed: true,
        images: [],
        accuracy: null,
        warnings: [],
        warningsLen: null,
        reseter: null,
        alert: false
      }
    },
    computed: {
      form () {
        return {
          GT_dataset: this.GT_dataset
        }
      },
      isInitial () {
        return this.currentStatus === STATUS_INITIAL
      },
      isEvaluate () {
        return this.currentStatus === STATUS_EVALUATING
      },
      isSuccess () {
        return this.currentStatus === STATUS_SUCCESS
      },
      isFailed () {
        return this.currentStatus === STATUS_FAILED
      }
    },
    methods: {
      getDatasetOptions () {
        this.options = this.getDatasetOptionsFromBackend()
      },
      getDatasetOptionsFromBackend () {
        const path = `http://localhost:5000/api/getoptions`
        axios.get(path)
          .then(response => {
            this.options = response.data.options
          })
          .catch(error => {
            console.log(error)
          })
      },
      filesChange (fieldName, fileList) {
        const formData = new FormData()
        if (!fileList.length) return
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append(fieldName, fileList[x], fileList[x].name)
          })
        this.formData = formData
        if (this.GT_dataset !== '') {
          this.evaluateEnable = true
        }
      },
      evaluate () {
        this.rows = []
        this.currentStatus = STATUS_EVALUATING
        this.formData.append('GT_dataset', this.GT_dataset)
        upload(this.formData, 'evaluate_dataset')
          .then(x => {
            if (x.return === 0) {
              this.currentStatus = STATUS_SUCCESS
              this.CM = x.result
              this.CMTable = x.table
              this.detailedTable = x.detailedTable
              this.images = x.images
              this.accuracy = x.accuracy
              this.warnings = x.warnings
              this.warningsLen = this.warnings.length
            } else {
              this.currentStatus = STATUS_FAILED
              this.uploadError = x.msg
            }
          })
          .catch(err => {
            console.log(err.response)
            this.uploadError = err.response
          })
      },
      isActive () {
        if (this.formData && this.GT_dataset) {
          this.evaluateEnable = true
        }
      },
      reset () {
        // reset form to initial state
        this.uploadError = ''
        this.uploadError = null
        this.GT_dataset = ''
        this.Algorithm_dataset = ''
        this.evaluateEnable = false
        this.formData = null
        this.CM = null
        this.CMTable = null
        this.detailedTable = null
        this.showCM = true
        this.showDetailed = true
        this.accuracy = null
        this.warnings = []
        this.alert = false
        this.warningsLen = null
        const path = `http://localhost:5000/api/remove_frontend_files`
        axios.get(path)
          .then(response => {
          })
          .catch(error => {
            console.log(error)
          })
        this.currentStatus = STATUS_INITIAL
      },
      showCMTable () {
        if (this.showCM) {
          document.getElementById('CMtable').innerHTML = this.CMTable
        } else {
          document.getElementById('CMtable').innerHTML = null
        }
      },
      showDetailedTable () {
        if (this.showDetailed) {
          document.getElementById('Detailedtable').innerHTML = this.detailedTable
          var i = 0
          for (var j = 0; j < this.images.length; ++j) {
            document.getElementById('row ' + i).innerHTML = '<img style="display: block;width:80%;" src=' + this.images[j] + '>'
            i++
          }
        } else {
          document.getElementById('Detailedtable').innerHTML = null
        }
      }
    }
  }
</script>

<style scoped>
  .accuracy {
    display: inline;
    padding-left: 40%;
    font-size: large;
    font-weight: bold;
  }
</style>

<!--@click="reset()"-->
