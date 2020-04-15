import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import DatasetManager from '@/components/DatasetManager'
import Uploader from '@/components/Uploader'
import Evaluator from '@/components/Evaluator'
import ReportManager from '@/components/ReportManager'
import ReportView from '@/components/ReportView'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/report/:component_name', name: 'component_name', component: ReportManager },
    { path: '/report/:component_name/report_view', name: 'component_name', component: ReportView },
    { path: '/dataset_manager', name: 'dataset_manager', component: DatasetManager },
    { path: '/uploader', name: 'uploader', component: Uploader },
    { path: '/evaluator', name: 'evaluator', component: Evaluator }
  ]
})
