import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import ReportManager from '@/components/ReportManager'
import ReportView from '@/components/ReportView'
import RunnerManager from '@/components/RunnerManager'
import Uploader from '@/components/Uploader'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/report/:component_name', name: 'component_name', component: ReportManager },
    { path: '/report/:component_name/report_view', name: 'report_view', component: ReportView },
    { path: '/runner/:run_type', name: 'run_type', component: RunnerManager },
    { path: '/uploader', name: 'uploader', component: Uploader }
  ]
})
