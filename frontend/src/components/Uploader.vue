<template>
  <div id="uploader">
    <v-container fluid style="margin-top: 3%">
      <v-layout row wrap>
        <v-flex xs12 md6 offset-md3>
          <v-card>
            <v-toolbar dark>
              <v-toolbar-title>Dataset Uploader</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <div v-if="isInitial || isSaving">
                  <v-text-field
                    v-model="datasetName"
                    :rules="[() => datasetName.length > 0 || 'This field is required']"
                    label="Dataset name"
                    class="mt-5"
                    color="black"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="datasetTags"
                    :rules="[() => datasetTags.length > 0 || 'This field is required']"
                    label="Tags separated by comma"
                    multi-line
                    color="black"
                    required
                  ></v-text-field>
                  <v-container center grid-list-xl>
                    <v-layout row>
                      <v-flex xs8>
                        <div class="container">
                            <h1>Upload images</h1>
                            <div class="dropbox">
                              <input type="file" multiple
                                     :name="uploadFieldName"
                                     :disabled="isSaving"
                                     @change="filesChange($event.target.name, $event.target.files)"
                                     >
                            </div>
                        </div>
                      </v-flex>
                    </v-layout>
                  </v-container>
                  <v-btn
                    :disabled="!valid"
                    @click="submit"
                  >
                    submit
                  </v-btn>
                  <v-btn @click="clear()">clear</v-btn>
                </div>
                <div v-else>
                  <div>
                    <h2 v-if="isSuccess">Upload Succeed</h2>
                    <div v-if="isFailed">
                      <h2>Upload Failed</h2>
                      <p>Error massage: {{ uploadError }}</p>
                    </div>
                  </div>
                  <p>
                    <v-btn
                      color="orange lighten-5"
                      @click="reset()"
                      block
                    >
                      Upload again
                    </v-btn>
                  </p>
                </div>
              </v-form>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>

  </div>
</template>

<script>
  // eslint-disable-next-line

  import {upload} from '../scripts/file-upload.service'

  const STATUS_INITIAL = 0
  const STATUS_SAVING = 1
  const STATUS_SUCCESS = 2
  const STATUS_FAILED = 3

  export default {
    name: 'Uploader',
    data () {
      return {
        submitted: false,
        valid: false,
        datasetName: '',
        datasetTags: '',
        uploadedFiles: [],
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'photos',
        formData: null
      }
    },
    computed: {
      isInitial () {
        return this.currentStatus === STATUS_INITIAL
      },
      isSaving () {
        return this.currentStatus === STATUS_SAVING
      },
      isSuccess () {
        return this.currentStatus === STATUS_SUCCESS
      },
      isFailed () {
        return this.currentStatus === STATUS_FAILED
      }
    },
    methods: {
      reset () {
        // reset form to initial state
        this.currentStatus = STATUS_INITIAL
        this.uploadedFiles = []
        this.uploadError = null
        this.datasetName = ''
        this.datasetTags = ''
        this.valid = false
        this.formData = null
      },
      save (formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING

        upload(formData, 'upload_dataset')
          .then(x => {
            if (x.return === 0) {
              this.currentStatus = STATUS_SUCCESS
            } else {
              this.currentStatus = STATUS_FAILED
              this.uploadError = x.msg
            }
          })
          .catch(err => {
            this.uploadError = err.response
          })
      },
      filesChange (fieldName, fileList) {
        // handle file changes
        const formData = new FormData()

        if (!fileList.length) return

        // append the files to FormData
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append(fieldName, fileList[x], fileList[x].name)
          })
        formData.append('name', this.datasetName)
        formData.append('tags', this.datasetTags)
        this.formData = formData
      },
      submit () {
        if (this.$refs.form.validate()) {
          this.save(this.formData)
        }
      },
      clear () {
        this.$refs.form.reset()
      }
    },
    mounted () {
      this.reset()
    }
  }
</script>

<style scoped>


</style>
