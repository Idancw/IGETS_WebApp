import * as axios from 'axios'

const BACKEND_URL = 'http://localhost:5000'

function upload (formData, uploadType) {
  const url = `${BACKEND_URL}/api/upload/` + uploadType
  return axios.post(url, formData)
  // get data
    .then(x => x.data)
}

export { upload }
