<template>
  <v-container id="RunnerManager" fluid grid-list-xl style="max-width: 90%; padding-top: 5%; padding-bottom: 5%">

    <h1 class="d-inline-block">{{runnerName}} Property File Definitions</h1>
    <v-btn
      class="right"
      :disabled="!(component !== '' && golden !== '' && candidate !== '')"
      color="teal accent-3"
      style="margin-bottom: 1%"
      @click="submit"
    >Run {{runnerName}}</v-btn>

    <div>
      <v-dialog
      v-model="showDialogMessage"
      width="500"
      >
        {{dialogMessage}}
      </v-dialog>
    </div>

    <v-form ref="form" v-model="valid">
      <v-select
        v-model="component"
        :items="componentOptions"
        label="Component Name"
        v-on:change="getVersions($event)"
        required
      ></v-select>
      <div class="d-flex">
        <v-select
          v-model="golden"
          :items="goldenOptions"
          label="Release Version"
          :disabled="versionDisable"
          required
        ></v-select>
        <v-select
          v-model="candidate"
          :items="candidateOptions"
          label="Candidate Version"
          :disabled="versionDisable"
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
        <div class="d-inline-block" style="width: 15%">
          <v-switch
            v-model="useCustomization"
            :label="templateSwitchName"
            color="purple accent-4"
            :value="useCustomization"
            :hint="'Switch to use ' + switchUsing"
            persistent-hint
            v-on:click="changeTemplateSwitch"
          ></v-switch>
        </div>
        <div v-if="useCustomization">
          <h2 style="display: inline-block">Filter</h2>
          <v-btn
            fab
            color="deep-purple accent-1"
            @click="addFilterBlock"
            style="margin-bottom: 1%"
            small
          ><v-icon>library_add</v-icon>
          </v-btn>
          <div class="FilterBlocks">
            <div v-for="(filterBlock, filterBlockIndex) in filterBlocks" style="display: inline-block; padding-right: 1%; margin-bottom: 1%">
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
                  color="purple accent-4"
                  :value="filterBlockIndex"
                  v-on:change="updateVisibility(filterBlockIndex, 'Exclude')"
                ></v-switch>
                <v-switch
                  style="position: absolute; margin-left: 7%; max-width: 200px"
                  v-model="visibleMultiplyIndexes"
                  hint="Multiply"
                  persistent-hint
                  color="purple accent-4"
                  :value="filterBlockIndex"
                  v-on:change="updateVisibility(filterBlockIndex, 'Multiply')"
                ></v-switch>
              </v-card-title>
              <div class="innerFilterBlocks">
                <v-card class="d-inline-block" v-for="(innerFilterBlock, innerFilterBlockName) in filterBlock">
                  <v-card-title v-if="innerFilterBlock.visible">{{innerFilterBlockName}}</v-card-title>
                  <v-card
                  class="d-flex"
                  color="grey lighten-4"
                  tile
                  v-for="(filterOption, filterOptionName) in innerFilterBlock" v-if="filterOptionName !== 'visible' && innerFilterBlock.visible"
                  >
                    <div>
                      <v-card-title class="font-weight-bold mb-1" style="width: 150px; max-width: 150px">{{filterOptionName}}</v-card-title>
                      <v-btn
                        small
                        color="deep-purple lighten-5"
                        fab
                        @click="addFilterOperator(filterBlockIndex, innerFilterBlockName, filterOptionName)"
                    ><v-icon>add</v-icon></v-btn>
                    </div>
                    <v-card
                      tile
                      v-for="operatorObj in filterOption"
                    >
                      <div v-if="filterOptionName !== 'Other'">
                        <v-select
                          v-if="filterOptionName !== 'Other'"
                          :items="operatorOptions"
                          v-model="operatorObj.operator"
                          label="Operator"
                          chips>
                        </v-select>
                        <div v-if="filterOptionName === 'CaseID'">
                          <v-text-field required :rules="[rules.isInteger]" label="Value" rows="1" v-model="operatorObj.value"></v-text-field>
                        </div>
                        <div v-else>
                          <v-text-field label="Value" rows="1" v-model="operatorObj.value"></v-text-field>
                        </div>
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
        valid: false,
        showDialogMessage: false,
        dialogMessage: '',
        useCustomization: false,
        templateSwitchName: 'Using Template',
        switchUsing: 'customization',
        runnerName: '',
        component: '',
        golden: '',
        candidate: '',
        debugLevel: '',
        componentOptions: [],
        goldenOptions: [],
        candidateOptions: [],
        debugLevelOptions: ['Debug', 'Info', 'Warning', 'Error'],
        versionDisable: true,
        numberOfBlocks: 1,
        filterBlocks: {},
        visibleExcludeIndexes: [],
        visibleMultiplyIndexes: [],
        visible: false,
        operator: '',
        operatorOptions: [],
        rules: {
          isInteger (value) {
            if (/^[0-9]*$/.test(value)) {
              return true
            }
            return 'Value must be an integer'
          }
        }
      }
    },
    created () {
      this.runnerName = this.$route.path.split('/')[this.$route.path.split('/').length - 1]
      this.operatorOptions = ['<', '>', '<=', '>=', '!=', '=', '~', '!~']
      this.getComponentNamesFromBackend()
    },
    methods: {
      getComponentNamesFromBackend () {
        const path = `${BACKEND_URL}/api/get_component_names`
        axios.get(path)
          .then(response => {
            this.componentOptions = response.data.result
          })
          .catch(error => {
            console.log(error)
          })
      },
      getVersions (component) {
        const path = `${BACKEND_URL}/api/get_component_versions/` + component
        axios.get(path)
          .then(response => {
            this.goldenOptions = response.data.result
            this.candidateOptions = response.data.result
          })
          .catch(error => {
            console.log(error)
          })
        this.versionDisable = false
        this.reset()
      },
      addFilterBlock () {
        let include = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: true}  // filterInnerBlock
        let exclude = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false}  // filterInnerBlock
        let multiply = {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false}  // filterInnerBlock
        let filters = [include, exclude, multiply]
        for (let index in filters) {
          if (filters.hasOwnProperty(index)) {
            filters[index].CaseID.push({operator: '', value: ''})
            filters[index].VersionNumber.push({operator: '', value: ''})
            filters[index].YamlCaseID.push({operator: '', value: ''})
            filters[index].Other.push({operator: '', value: ''})
          }
        }
        this.filterBlocks[this.numberOfBlocks] = {Include: include, Exclude: exclude, Multiply: multiply}
        this.visibleExcludeIndexes.push(this.numberOfBlocks)
        this.visibleMultiplyIndexes.push(this.numberOfBlocks)
        this.numberOfBlocks++
        this.visible = !this.visible
      },
      addFilterOperator (filterBlockIndex, innerFilterBlockName, filterOptionName) {
        this.filterBlocks[filterBlockIndex][innerFilterBlockName][filterOptionName].push({operator: '', value: ''})
        this.visible = !this.visible
      },
      updateVisibility (id, section) {
        this.filterBlocks[id][section].visible = !this.filterBlocks[id][section].visible
      },
      changeTemplateSwitch () {
        this.useCustomization = !this.useCustomization
        if (this.useCustomization) {
          this.templateSwitchName = 'Using Customization'
          this.switchUsing = 'template'
        } else {
          this.templateSwitchName = 'Using Template'
          this.switchUsing = 'customization'
        }
      },
      submit () {
        let formData = new FormData()

        formData.append('componentName', this.component)
        formData.append('goldenVersion', this.golden)
        formData.append('candidateVersion', this.candidate)
        let debugLevel = 'D'
        if (this.debugLevel !== '') {
          switch (this.debugLevel) {
            case 'Debug': debugLevel = 'D'
              break
            case 'Info': debugLevel = 'I'
              break
            case 'Warning': debugLevel = 'W'
              break
            case 'Error': debugLevel = 'E'
              break
          }
        }
        formData.append('debugLevel', debugLevel)
        if (!this.useCustomization) {  // meaning using template
          let filterBlocks = {'1': {}}
          let templateFilterBlock = {
            Include: {CaseID: [{operator: '>', value: '0'}], VersionNumber: [], YamlCaseID: [], Other: [], visible: true},
            Exclude: {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false},
            Multiply: {CaseID: [], VersionNumber: [], YamlCaseID: [], Other: [], visible: false}}
          filterBlocks['1'] = templateFilterBlock
          formData.append('filterBlocks', JSON.stringify(filterBlocks))
        } else {
          formData.append('filterBlocks', JSON.stringify(this.filterBlocks))
        }
        const url = `${BACKEND_URL}/api/run/` + this.runnerName
        axios.post(url, formData).then(x => this.dialogMessage = x.data.msg)
        console.log(this.dialogMessage)
        this.showDialogMessage = true
        this.reset()
      },
      reset () {
        this.component = ''
        this.golden = ''
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
