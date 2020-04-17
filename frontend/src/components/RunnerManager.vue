<template>
  <v-container id="RunnerManager" fluid grid-list-xl style="max-width: 90%; padding-top: 5%; padding-bottom: 5%">
    <h1>{{runnerName}} Property File Definitions</h1>

    <v-form ref="form">
      <v-select
        v-model="component"
        :items="componentOptions"
        label="Component Name"
        v-on:change="getVersions($event)"
        solo
        required
      ></v-select>
      <div class="d-flex">
        <v-select
          v-model="release"
          :items="releaseOptions"
          label="Release Version"
          :disabled="versionDisable"
          solo
          required
        ></v-select>
        <v-select
          v-model="candidate"
          :items="candidateOptions"
          label="Candidate Version"
          :disabled="versionDisable"
          solo
          required
        ></v-select>
      </div>
      <v-select
        v-model="debugLevel"
        :items="debugLevelOptions"
        label="Debug Level (optional)"
      ></v-select>
      <div v-if="runnerName === 'Regression'">
        <v-divider></v-divider>
        <h2 style="display: inline-block">Filter</h2>
          <v-btn
            fab
            color="deep-purple accent-1"
            @click="addFilterBlock"
            style="margin-bottom: 1%"
            small
          ><v-icon>library_add</v-icon>
          </v-btn>
        <div>
          <div v-for="(filterBlockOption, filterBlockIndex) in filterBlocks" style="display: inline-block; padding-right: 1%; margin-bottom: 1%">
            <v-card-title style="background-color: #D1C4E9">
              <span class="BlockTitle">
                Block {{filterBlockIndex}}
              </span>
              <v-spacer></v-spacer>
              <v-switch
                style="position: absolute; margin-left: 4%; max-width: 200px"
                v-model="visibleExcludeIndexes"
                hint="Exclude"
                persistent-hint
                color="red"
                :value="filterBlockIndex"
                v-on:change="updateVisibility(filterBlockIndex, 'Exclude')"
              ></v-switch>
              <v-switch
                style="position: absolute; margin-left: 7%; max-width: 200px"
                v-model="visibleMultiplyIndexes"
                hint="Multiply"
                persistent-hint
                color="red"
                :value="filterBlockIndex"
                v-on:change="updateVisibility(filterBlockIndex, 'Multiply')"
              ></v-switch>
            </v-card-title>

            <div>
              <v-card class="d-inline-block" v-for="(innerFilterBlock, innerFilterBlockName) in filterBlockOption">
                <v-card-title v-if="innerFilterBlock.visible">{{innerFilterBlockName}}</v-card-title>
                <v-card
                class="d-flex"
                color="grey lighten-4"
                tile
                v-for="(filterOption, filterOptionName) in innerFilterBlock" v-if="filterOptionName !== 'visible' && innerFilterBlock.visible"
                >
                  <div>
                    <v-card-title class="font-weight-bold mb-1" style="width: 150px; max-width: 150px" v-if="innerFilterBlock.visible">{{filterOptionName}}</v-card-title>
                    <v-btn
                      small
                      round
                      color="deep-purple lighten-5"
                      fab
                      @click="addFilterOperand(filterBlockIndex, innerFilterBlockName, filterOptionName)"
                  ><v-icon>add</v-icon></v-btn>
                  </div>
                  <v-card
                    outlined
                    tile
                    v-for="operatorObj in filterOption"
                  >
                    <div v-if="visible"></div>
                    <div v-if="filterOptionName !== 'Other'">
                      <v-select
                        v-if="filterOptionName !== 'Other'"
                        :items="operatorOptions"
                        v-model="operatorObj.operand"
                        label="Operator"
                        chips>
                      </v-select>
                      <v-text-field label="Value" rows="1" v-model="operatorObj.value"></v-text-field>
                    </div>
                    <div v-else>
                      <v-text-field label="Value" rows="2" multi-line auto-grow v-model="operatorObj.value"></v-text-field>
                    </div>

                  </v-card>
                </v-card>
              </v-card>
            </div>
          </div>
        </div>
        <div v-if="visible"></div>
      </div>
      <div v-else>

      </div>
    </v-form>


  </v-container>
</template>

<script>
  import axios from 'axios'
  // CONST backend Url
  let BACKEND_URL = 'http://localhost:5000'

  export default {
    name: 'RunnerManager',
    data () {
      return {
        runnerName: '',
        component: '',
        release: '',
        candidate: '',
        debugLevel: '',
        componentOptions: [],
        releaseOptions: [],
        candidateOptions: [],
        debugLevelOptions: ['Debug', 'Info', 'Warning', 'Error'],
        versionDisable: true,
        numberOfBlocks: 1,
        filterBlocks: {},
        visibleExcludeIndexes: [],
        visibleMultiplyIndexes: [],
        visible: false,
        operator: '',
        operatorOptions: []
      }
    },
    created () {
      this.runnerName = this.$route.path.split('/')[this.$route.path.split('/').length - 1]
      this.operatorOptions = ['<', '>', '<=', '>=']
      this.getComponentNamesFromBackend()
    },
    methods: {
      getComponentNamesFromBackend () {
        const path = `${BACKEND_URL}/api/get_component_names`
        axios.get(path)
          .then(response => {
            this.componentOptions = response.data.component_names
          })
          .catch(error => {
            console.log(error)
          })
      },
      getVersions (component) {
        const path = `${BACKEND_URL}/api/get_component_versions/` + component
        axios.get(path)
          .then(response => {
            this.releaseOptions = response.data.result
            this.candidateOptions = response.data.result
          })
          .catch(error => {
            console.log(error)
          })
        this.versionDisable = false
        this.reset()
      },
      addFilterBlock () {
        let include = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: true}
        let exclude = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false}
        let multiply = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false}
        let filters = [include, exclude, multiply]
        for (let index in filters) {
          if (filters.hasOwnProperty(index)) {
            filters[index].CaseID.push({operand: '', value: ''})
            filters[index].VersionNumber.push({operand: '', value: ''})
            filters[index].YamlCaseID.push({operand: '', value: ''})
            filters[index].Other.push({operand: '', value: ''})
          }
        }
        this.filterBlocks[this.numberOfBlocks] = {Include: include, Exclude: exclude, Multiply: multiply}
        this.visibleExcludeIndexes.push(this.numberOfBlocks)
        this.visibleMultiplyIndexes.push(this.numberOfBlocks)
        this.numberOfBlocks++
        this.visible = !this.visible
      },
      addFilterOperand (index, filterBlock, filterOption) {
        this.filterBlocks[index][filterBlock][filterOption].push({operand: '', value: ''})
        console.log(this.filterBlocks[index])
        this.visible = !this.visible
      },
      updateVisibility (id, section) {
        this.filterBlocks[id][section].visible = !this.filterBlocks[id][section].visible
      },
      reset () {
        this.release = ''
        this.candidate = ''
        this.debugLevel = ''
        this.filterBlocks = {}
        this.numberOfBlocks = 1
      }
    },
    watch: {
      $route (to, from) {
        this.runnerName = this.$route.path.split('/')[this.$route.path.split('/').length - 1]
        this.reset()
      }
    }
  }
</script>

<style scoped>

</style>
