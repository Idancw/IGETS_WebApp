<template>
  <div id="app">
    <v-app light>
      <v-content>
        <section>
          <v-parallax src="https://freedesignfile.com/upload/2017/01/Light-blue-tech-background-vector-05.jpg"
                      style="padding: 5%">
            <v-layout column align-center justify-center class="white--text">
              <h1 class="white--text mb-2 display-1 text-xs-center" style="font-size: 76px!important;">
                IGETS Tool
              </h1>
              <h3 style="margin-top: 1%">Image Generation Engine Test Suite</h3>
            </v-layout>
          </v-parallax>
        </section>

        <section>
          <v-layout column wrap class="my-5" align-center>
            <pre class="text-xs-center" style="font-family: unset; font-size: 30px; margin-bottom: -40px; white-space: pre-line;">
              This tool provides easy way to view and run DevOps tools and results
            </pre>
          </v-layout>
        </section>
        <br>
        <hr>
        <section>
          <v-layout column wrap class="my-5" align-center>
            <v-flex xs12 sm4 class="my-3">
              <div class="text-xs-center">
                <h2 class="mb-3 text-xs-center">All in one tool</h2>
              </div>
            </v-flex>
            <v-flex xs12>
              <v-container grid-list-xl>
                <v-layout row wrap align-center>
                  <v-flex xs12 md4 style="margin-bottom: 80px;">
                    <v-card class="elevation-0 transparent">
                      <v-card-text class="text-xs-center">
                        <v-icon x-large class="blue--text text--lighten-2">cloud_upload</v-icon>
                      </v-card-text>
                      <v-card-title primary-title class="layout justify-center">
                        <div class="headline text-xs-center">Dataset Uploader</div>
                      </v-card-title>
                      <v-card-text style="text-align: justify;">
                        The Dataset Uploader allows the easy creation of a dataset while allowing the
                        user to name the dataset, create the tags that will be used for it and
                        upload the images that will be tagged with the purpose of creating a ground truth.
                      </v-card-text>
                    </v-card>
                   </v-flex>
                  <v-flex xs12 md4>
                    <v-card class="elevation-0 transparent">
                      <v-card-text class="text-xs-center">
                        <v-icon x-large class="blue--text text--lighten-2">how_to_reg</v-icon>
                      </v-card-text>
                      <v-card-title primary-title class="layout justify-center">
                        <div class="headline">Dataset Manager</div>
                      </v-card-title>
                      <v-card-text style="text-align: justify;">
                        The Dataset Manager allows the user to load a dataset which consists of instances
                        of images and a set of tags. The user can than choose for each instance the correct
                        tags that best describe it. The Dataset Manager offers the user a convenient interface
                        which allows an easy way to save the current state of the dataset and the ability to
                        clear the already tagged instances from the Dataset Manager page or show it again.
                      </v-card-text>
                    </v-card>
                  </v-flex>
                  <v-flex xs12 md4 style="margin-bottom: 43px;">
                    <v-card class="elevation-0 transparent">
                      <v-card-text class="text-xs-center">
                        <v-icon x-large class="blue--text text--lighten-2">perm_data_setting</v-icon>
                      </v-card-text>
                      <v-card-title primary-title class="layout justify-center">
                        <div class="headline text-xs-center">Evaluator</div>
                      </v-card-title>
                      <v-card-text style="text-align: justify;">
                        The Evaluator allows the user to compare between a ground truth set (tagged set of images)
                        and the output of a classification algorithm. The Evaluator creates a confusion matrix
                        comparing between the algorithm and the ground truth as well as a convenient display of
                        the images along with the result of the comparison for each instance.
                      </v-card-text>
                    </v-card>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-flex>
          </v-layout>

          <v-layout row wrap justify-center class="my-5">
            <v-flex >
              <v-card class="elevation-0 transparent">
                <v-list class="transparent">
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title style="padding-left: 20%">
                        <div style="display: inline">
                          <img src="https://image.flaticon.com/icons/svg/25/25231.svg"style="width:15px;height:15px;">
                          <a href="https://github.com/Idancw/IndustrialProject" target="_blank" class="align-middle">
                            GitHub
                          </a>
                        </div>
                      </v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
              </v-card>
            </v-flex>
          </v-layout>
        </section>

      </v-content>
    </v-app>
  </div>
</template>

<script>
  export default {
    name: 'home',
    data () {
      return {
        title: 'IGETS Tool'
      }
    }
  }
</script>

<style scoped>
  a {
    text-decoration: none !important;
    color: #000;
    font-size: 18px;
  }
  hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
    width: 90%;
    margin-left: 5%;
  }
</style>
