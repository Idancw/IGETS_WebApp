import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import DatasetManager from '@/components/DatasetManager'
import Uploader from '@/components/Uploader'
import Evaluator from '@/components/Evaluator'
import ComponentReportViewer from '@/components/ComponentReportViewer'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/report/:component_name', name: 'component_name', component: ComponentReportViewer },
    { path: '/dataset_manager', name: 'dataset_manager', component: DatasetManager },
    { path: '/uploader', name: 'uploader', component: Uploader },
    { path: '/evaluator', name: 'evaluator', component: Evaluator }
  ]
})
