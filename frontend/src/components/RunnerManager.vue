<template>
  <v-container id="RunnerManager" fluid grid-list-xl style="max-width: 78%; padding-top: 5%">
    <h1>{{runnerName}} Property File Definitions</h1>

    <v-form ref="form">
      <v-select
        v-model="component"
        :items="componentOptions"
        label="Component Name"
        v-on:change="getVersions($event)"
        required
      ></v-select>
      <!--      TODO: do versions in one line-->
        <v-select
          v-model="release"
          :items="releaseOptions"
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
      <!--      -->
      <v-select
        v-model="debugLevel"
        :items="debugLevelOptions"
        label="Debug Level (optional)"
      ></v-select>
      <div v-if="runnerName === 'Regression'">
        <v-divider></v-divider>
        <h2 style="display: inline-block">Filter</h2>
        <!--        TODO: Make the btn small-->
          <v-btn
            fab
            color="deep-purple accent-1"
            @click="addFilterBlock"
            style="margin-bottom: 1%"
          ><v-icon>library_add</v-icon>
          </v-btn>
        <!---->
        <div>
          <div v-for="(blockInfo, id) in filterBlocks" style="display: inline-block; padding-right: 1%; margin-bottom: 1%">
            <v-card-title style="background-color: #D1C4E9">
              <span class="BlockTitle">
                Block {{id}}
              </span>
              <v-spacer></v-spacer>
              <v-switch
                style="position: absolute; margin-left: 4%"
                v-model="visibleExcludeIndexes"
                hint="Exclude"
                persistent-hint
                color="red"
                :value="id"
                v-on:change="updateVisibility(id, 'Exclude')"
              ></v-switch>
              <v-switch
                style="position: absolute; margin-left: 7%"
                v-model="visibleMultiplyIndexes"
                hint="Multiply"
                persistent-hint
                color="red"
                :value="id"
                v-on:change="updateVisibility(id, 'Multiply')"
              ></v-switch>
            </v-card-title>
            <v-card class="d-inline-block mx-auto" v-for="(innerBlock, field) in blockInfo">
              <v-card-subtitle v-if="innerBlock.visible">{{field}}</v-card-subtitle>
              <div v-for="(index, title) in innerBlock" v-if="title !== 'visible' && innerBlock.visible">
                {{title}}
                <v-select
                  :items="operatorOptions"
                  label="Operator"
                  chips
                ></v-select>

              </div>
<!--              <v-text-field v-for="(index, title) in innerBlock" v-if="title !== 'visible' && innerBlock.visible"-->
<!--                            :label="title"-->
<!--                            multi-line-->
<!--                            rows="1"-->
<!--                            auto-grow-->
<!--                            clearable-->
<!--                ></v-text-field>-->
              </v-card>
          </div>
        </div>
        <div v-if="visible"></div>
      </div>
      <div v-else>

      </div>
<!--      <v-btn-->
<!--        :disabled="!valid"-->
<!--        color="success"-->
<!--        class="mr-4"-->
<!--        @click="validate"-->
<!--      >-->
<!--        Validate-->
<!--      </v-btn>-->

<!--      <v-btn-->
<!--        color="error"-->
<!--        class="mr-4"-->
<!--        @click="reset"-->
<!--      >-->
<!--        Reset Form-->
<!--      </v-btn>-->

<!--      <v-btn-->
<!--        color="warning"-->
<!--        @click="resetValidation"-->
<!--      >-->
<!--        Reset Validation-->
<!--      </v-btn>-->
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
        let include = {CaseID: [], VersionNumber: [], YamlCaseID: [], visible: true}
        let exclude = {CaseID: [], VersionNumber: [], YamlCaseID: [], visible: false}
        let multiply = {CaseID: [], VersionNumber: [], YamlCaseID: [], visible: false}
        this.filterBlocks[this.numberOfBlocks] = {Include: include, Exclude: exclude, Multiply: multiply}
        this.visibleExcludeIndexes.push(this.numberOfBlocks)
        this.visibleMultiplyIndexes.push(this.numberOfBlocks)
        this.numberOfBlocks++
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
