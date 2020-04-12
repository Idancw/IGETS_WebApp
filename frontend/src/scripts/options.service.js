import * as axios from 'axios'

const BASE_URL = 'http://localhost:5000'

function getDatasetOptionsFromBackend () {
  const url = `${BASE_URL}/api/getoptions`
  return axios.get(url)
    .then(response => response.data.options)
    .catch(error => {
      console.log(error)
    })
}

export { getDatasetOptionsFromBackend }
